"""
Copyright © 2020-2025 Ralph Seichter

This file is part of "Fangfrisch".

Fangfrisch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fangfrisch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Fangfrisch. If not, see <https://www.gnu.org/licenses/>.
"""

import re
import sys
from datetime import datetime
from datetime import timedelta
from typing import List
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fangfrisch import ClamavItem
from fangfrisch.config.config import config
from fangfrisch.log import log_debug
from fangfrisch.log import log_exception
from fangfrisch.log import log_fatal
from fangfrisch.util import remove_if_exists

DB_VERSION = 2
Base = declarative_base()


class DbMeta(Base):
    __tablename__ = "automx2"
    db_version = Column(Integer, nullable=False, primary_key=True)
    _engine = None
    _session = None

    def __init__(self) -> None:
        self.db_version = DB_VERSION

    @classmethod
    def init(cls, create_all=False, drop_all=False):
        """Initialise database session.

        :param create_all: Create DB structure?
        :param drop_all: Drop existing DB structure?
        """
        if not cls._session:
            db_url = config.db_url()
            if not db_url:  # pragma: no cover
                log_fatal("Database URL is undefined, exiting.")
                sys.exit(1)
            cls._engine = create_engine(db_url, echo=False)
            cls._session = sessionmaker(bind=cls._engine)
        if drop_all:
            cls.metadata.drop_all(cls._engine)
        if create_all:
            cls.metadata.create_all(cls._engine)
        return cls._session

    @staticmethod
    def assert_version_match() -> Optional[bool]:
        try:
            DbMeta.init(False)
            session = DbMeta._session()
            dm: DbMeta = session.query(DbMeta).one()
            if dm.db_version == DB_VERSION:
                return True
            log_fatal(f"Unexpected database version (expected {DB_VERSION}, got {dm.db_version})")
        except DatabaseError as e:
            log_exception(e)
        log_fatal('Please try running "initdb"')
        sys.exit(1)

    def create_metadata(self, force=False) -> Optional[bool]:
        try:
            DbMeta.init(create_all=True, drop_all=force)
            with DbMeta._session() as session, session.begin():
                # Unless exceptions occur, the inner context calls session.commit()
                # and the outer context calls session.close().
                dm: DbMeta = session.query(DbMeta).first()
                if dm is None:
                    session.add(self)
                    return True
                log_fatal(f"Database table {self.__tablename__} is not empty")
        except DatabaseError as e:  # pragma: no cover
            log_exception(e)
        sys.exit(1)


class RefreshLog(Base):
    __tablename__ = "refreshlog"
    url = Column(String, nullable=False, primary_key=True)
    digest = Column(String, nullable=True)
    path = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    updated = Column(DateTime, nullable=True)
    _session = None

    def __init__(self, ci: ClamavItem, digest: str):
        self.digest = digest
        self.path = ci.path
        self.provider = ci.section
        self.updated = datetime.utcnow()
        self.url = ci.url

    @classmethod
    def init(cls):
        """Initialise database session."""
        if not cls._session:
            db_url = config.db_url()
            if not db_url:  # pragma: no cover
                log_fatal("Database URL is undefined, exiting.")
                sys.exit(1)
            engine = create_engine(db_url, echo=False)
            cls._session = sessionmaker(bind=engine)
        return cls._session

    @staticmethod
    def is_outdated(url: str, interval: int) -> bool:
        """Check if local data for a given URL is outdated.

        :param url: Log database key.
        :param interval: Maximum permitted age of local data.
        :return: True if outdated, False otherwise.
        """
        threshold = datetime.utcnow() - timedelta(minutes=interval)
        RefreshLog.init()
        with RefreshLog._session() as session:
            entry: RefreshLog = _query_url(url, session)
            return (entry is None) or entry.updated < threshold

    @staticmethod
    def digest_matches(url: str, digest: str) -> bool:
        """Check if locally recorded digest matches the provided value.

        :param url: Log database key.
        :param digest: Expected digest.
        :return: True if digests match, False otherwise.
        """
        RefreshLog.init()
        with RefreshLog._session() as session:
            entry: RefreshLog = _query_url(url, session)
            return (entry is not None) and entry.digest == digest

    @staticmethod
    def last_logged_path(url: str) -> Optional[str]:
        """Return previously recorded file path for the given URL.

        :param url: Log database key.
        :return: Recorded file path if available, None otherwise.
        """
        RefreshLog.init()
        with RefreshLog._session() as session:
            entry: RefreshLog = _query_url(url, session)
            if entry is None:
                return None
            return entry.path

    @staticmethod
    def url_path_mappings(provider_re: str):
        """Return URL-to-localpath mappings for providers.

        :param provider_re: Provider name filter (regular expression)
        """
        RefreshLog.init()
        with RefreshLog._session() as session:
            return _query_provider_re(provider_re, session)

    @staticmethod
    def update(ci: ClamavItem, digest: str) -> None:
        """Update digest and update timestamp for a given URL.

        :param ci: Source data structure.
        :param digest: New digest.
        """
        RefreshLog.init()
        with RefreshLog._session() as session, session.begin():
            entry: RefreshLog = _query_url(ci.url, session)
            if entry:
                entry.digest = digest
                entry.path = ci.path
                entry.provider = ci.section
                entry.updated = datetime.utcnow()
            else:
                entry = RefreshLog(ci, digest)
                session.add(entry)

    @staticmethod
    def cleanup_provider(provider: str) -> int:
        """Cleanup local files associated with a given provider.

        :param provider: Provider filter (exact match)
        """
        count = 0
        RefreshLog.init()
        with RefreshLog._session() as session, session.begin():
            entries = _query_provider(provider, session)
            for entry in entries:
                remove_if_exists(entry.path, log_debug)
                session.delete(entry)
                count += 1
        return count


def _query_provider(provider: str, session) -> List[RefreshLog]:
    entries = list()
    r: RefreshLog
    for r in session.query(RefreshLog).filter(RefreshLog.provider == provider).all():
        entries.append(r)
    return entries


def _query_provider_re(regex: str, session) -> List[RefreshLog]:
    _re = re.compile(regex)
    entries = list()
    r: RefreshLog
    for r in session.query(RefreshLog).all():
        if _re.search(r.provider):
            entries.append(r)
    return entries


def _query_url(url: str, session):
    return session.query(RefreshLog).filter(RefreshLog.url == url).first()
