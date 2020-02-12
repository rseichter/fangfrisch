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
import unittest
from argparse import Namespace

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.refresh import ClamavItem
from fangfrisch.refresh import ClamavRefresh
from tests import FangfrischTest

HORUS_FEED = 'https://horus-it.com/feed.xml'
HORUS_INDEX = 'https://horus-it.com/index.html'
HORUS_ROBOTS = 'https://horus-it.com/robots.txt'

config.init(FangfrischTest.CONF)


class RefreshTests(FangfrischTest):
    ref = ClamavRefresh(Namespace(force=False))

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
        cr = ClamavRefresh(Namespace(force=True))
        self.assertEqual(2, cr.refresh_all())

    def test_refresh(self):
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.add(RefreshLog('https://horus-it.com/favicon-32x32.png'))
        self.s.commit()
        self.assertEqual(1, self.ref.refresh_all())


if __name__ == '__main__':
    unittest.main()
