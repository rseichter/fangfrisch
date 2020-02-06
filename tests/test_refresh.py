import unittest

from fangfrisch.config import config
from fangfrisch.refresh import UrlTuple
from fangfrisch.refresh import refresh
from fangfrisch.refresh import refresh_all
from tests import FangfrischTest

HORUS_FEED = 'https://horus-it.com/feed.xml'
HORUS_INDEX = 'https://horus-it.com/index.html'
HORUS_ROBOTS = 'https://horus-it.com/robots.txt'

config.init(FangfrischTest.CONF)


class RefreshTests(FangfrischTest):
    def test_404(self):
        ut = UrlTuple(self.UNITTEST, 'x', HORUS_INDEX + 'BAD', None, None)
        self.assertFalse(refresh(ut))

    def test_bad_checksum(self):
        ut = UrlTuple(self.UNITTEST, 'x', HORUS_INDEX, 'sha256', None)
        self.assertFalse(refresh(ut))

    def test_good_checksum(self):
        ut = UrlTuple(self.UNITTEST, 'x', HORUS_ROBOTS, 'sha256', f'{self.TMPDIR}/x')
        self.assertTrue(refresh(ut))

    def test_missing_checksum(self):
        ut = UrlTuple(self.UNITTEST, 'x', HORUS_FEED, 'sha256', None)
        self.assertFalse(refresh(ut))

    def test_unknown_check(self):
        ut = UrlTuple(self.UNITTEST, 'x', HORUS_INDEX, 'BAD', None)
        self.assertFalse(refresh(ut))

    @unittest.skipUnless(FangfrischTest.online_tests(), 'online tests disabled')
    def test_refresh_all(self):
        self.assertEqual(2, refresh_all())


if __name__ == '__main__':
    unittest.main()
