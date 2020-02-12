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
