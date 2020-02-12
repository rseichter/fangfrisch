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
import os
import sys
from datetime import datetime
from datetime import timedelta

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fangfrisch.logging import log

_url = os.getenv('SQLALCHEMY_URL')
if not _url:  # pragma: no cover
    log.error('SQLALCHEMY_URL is undefined')
    sys.exit(1)
_engine = create_engine(_url, echo=False)
Session = sessionmaker(bind=_engine)
Base = declarative_base()


class RefreshLog(Base):
    __tablename__ = 'refreshlog'
    url = Column(String, primary_key=True)
    refreshed = Column(DateTime)

    def __init__(self, url) -> None:
        self.url = url
        self.refreshed = datetime.utcnow()

    @staticmethod
    def _by_url(url, session):
        return session.query(RefreshLog).filter(RefreshLog.url == url).first()

    @staticmethod
    def refresh_required(url, max_age) -> bool:
        entry = RefreshLog._by_url(url, Session())
        if not entry:
            return True
        threshold = datetime.utcnow() - timedelta(minutes=max_age)
        return entry.refreshed < threshold

    @staticmethod
    def stamp_by_url(url) -> None:
        session = Session()
        entry = RefreshLog._by_url(url, session)
        if entry:
            entry.refreshed = datetime.utcnow()
        else:
            entry = RefreshLog(url)
        session.add(entry)
        session.commit()
