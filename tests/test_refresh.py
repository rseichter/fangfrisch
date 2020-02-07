import unittest

from fangfrisch.config import config
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
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX + 'BAD', None, None)
        self.assertFalse(self.ref.refresh(ci))

    def test_bad_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX, 'sha256', None)
        self.assertFalse(self.ref.refresh(ci))

    def test_good_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_ROBOTS, 'sha256', f'{self.TMPDIR}/x')
        self.assertTrue(self.ref.refresh(ci))

    def test_missing_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_FEED, 'sha256', None)
        self.assertFalse(self.ref.refresh(ci))

    def test_unknown_check(self):
        ci = ClamavItem(self.UNITTEST, 'x', HORUS_INDEX, 'BAD', None)
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(FangfrischTest.online_tests(), 'online tests disabled')
    def test_refresh_all(self):
        self.assertEqual(2, self.ref.refresh_all())


if __name__ == '__main__':
    unittest.main()
