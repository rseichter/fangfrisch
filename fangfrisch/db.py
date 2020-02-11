import os
import sys
from datetime import datetime

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
        super().__init__()
        self.url = url
        self.refreshed = datetime.utcnow()

    @staticmethod
    def stamp_by_url(url) -> None:
        session = Session()
        entry = session.query(RefreshLog).filter(RefreshLog.url == url).first()
        if not entry:
            entry = RefreshLog(url)
        entry.stamp()

    def stamp(self) -> None:
        self.refreshed = datetime.utcnow()
        session = Session()
        session.add(self)
        session.commit()
