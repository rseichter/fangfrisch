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

URL_BAD_SHA256 = 'https://seichter.de/favicon.ico'
URL_MD5 = 'https://seichter.de/favicon-32x32.png'
URL_MISSING = 'https://seichter.de/index.html'
URL_SHA256 = 'https://seichter.de/favicon-16x16.png'

config.init(FangfrischTest.CONF)


class RefreshTests(FangfrischTest):
    ref = ClamavRefresh(Namespace(force=False))

    def setUp(self) -> None:
        super().setUp()
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.commit()

    def test_404(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_BAD_SHA256 + 'BAD', None, None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_bad_sha256(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_BAD_SHA256, 'sha256', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_good_sha256(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_SHA256, 'sha256', f'{self.TMPDIR}/x', 0)
        self.assertTrue(self.ref.refresh(ci))

    def test_good_md5(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_MD5, 'md5', f'{self.TMPDIR}/x', 0)
        self.assertTrue(self.ref.refresh(ci))

    def test_missing_checksum(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_MISSING, 'sha256', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_unknown_check(self):
        ci = ClamavItem(self.UNITTEST, 'x', URL_BAD_SHA256, 'BAD', None, 0)
        self.assertFalse(self.ref.refresh(ci))

    def test_refresh_force(self):
        cr = ClamavRefresh(Namespace(force=True))
        self.assertEqual(3, cr.refresh_all())

    def test_refresh(self):
        self.s.add(RefreshLog(URL_MD5))
        self.s.commit()
        self.assertEqual(1, self.ref.refresh_all())


if __name__ == '__main__':
    unittest.main()
