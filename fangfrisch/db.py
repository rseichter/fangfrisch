"""
Copyright © 2020 Ralph Seichter

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
along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
import sys
from datetime import datetime
from datetime import timedelta

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fangfrisch.config.config import config
from fangfrisch.logging import log

Base = declarative_base()


class RefreshLog(Base):
    __tablename__ = 'refreshlog'
    url = Column(String, primary_key=True)
    refreshed = Column(DateTime)
    _session = None

    def __init__(self, url) -> None:
        self.url = url
        self.refreshed = datetime.utcnow()

    @classmethod
    def init(cls):
        if not cls._session:
            db_url = config.db_url()
            if not db_url:  # pragma: no cover
                log.fatal('Database URL is undefined')
                sys.exit(1)
            cls._session = sessionmaker(bind=create_engine(db_url, echo=False))

    @staticmethod
    def _by_url(url, session):
        return session.query(RefreshLog).filter(RefreshLog.url == url).first()

    @staticmethod
    def refresh_required(url, max_age) -> bool:
        RefreshLog.init()
        entry = RefreshLog._by_url(url, RefreshLog._session())
        if not entry:
            return True
        threshold = datetime.utcnow() - timedelta(minutes=max_age)
        return entry.refreshed < threshold

    @staticmethod
    def stamp_by_url(url) -> None:
        RefreshLog.init()
        session = RefreshLog._session()
        entry = RefreshLog._by_url(url, session)
        if entry:
            entry.refreshed = datetime.utcnow()
        else:
            entry = RefreshLog(url)
        session.add(entry)
        session.commit()
