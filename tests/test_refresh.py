import unittest

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.db import Session
from fangfrisch.refresh import ClamavItem
from fangfrisch.refresh import ClamavRefresh
from tests import FangfrischTest

HORUS_FEED = 'https://horus-it.com/feed.xml'
HORUS_INDEX = 'https://horus-it.com/index.html'
HORUS_ROBOTS = 'https://horus-it.com/robots.txt'

config.init(FangfrischTest.CONF)


class RefreshTests(FangfrischTest):
    ref = ClamavRefresh()

    def test_404(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX + 'BAD', None, None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_bad_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX, 'sha256', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_good_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_ROBOTS, 'sha256', f'{self.TMPDIR}/x', 0)
        self.assertTrue(self.ref.refresh(ci))

    def test_missing_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_FEED, 'sha256', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_unknown_check(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX, 'BAD', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_refresh_force(self):
        self.assertEqual(2, self.ref.refresh_all(force=True))

    def test_refresh(self):
        self.s = Session()
        self.s.query(RefreshLog).delete()
        self.s.add(RefreshLog('https://horus-it.com/favicon-32x32.png'))
        self.s.commit()
        self.assertEqual(1, self.ref.refresh_all(force=False))


if __name__ == '__main__':
    unittest.main()
