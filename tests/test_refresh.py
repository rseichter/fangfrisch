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
along with Fangfrisch. If not, see <https://www.gnu.org/licenses/>.
"""
import unittest
from argparse import Namespace
from datetime import timedelta

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.download import ClamavItem
from fangfrisch.refresh import ClamavRefresh
from tests import DIGEST_MD5
from tests import FangfrischTest
from tests import MAX_SIZE
from tests import URL_BAD_SHA256
from tests import URL_MD5
from tests import URL_MISSING
from tests import URL_SHA256

MINUTES_IN_TEN_YEARS = 10 * 365 * 24 * 60

config.init(FangfrischTest.CONF)


class _CI(ClamavItem):
    def __init__(self, section, option, url, check=None, path=None, max_age=0, max_size=MAX_SIZE) -> None:
        super().__init__(section, option, url, check, path, max_age, max_size)


class RefreshTests(FangfrischTest):
    ref = ClamavRefresh(Namespace(force=False))

    def setUp(self) -> None:
        super().setUp()
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.commit()

    def test_404(self):
        ci = _CI(self.UNITTEST, 'x', URL_BAD_SHA256 + 'BAD')
        self.assertFalse(self.ref.refresh(ci))

    def test_bad_sha256(self):
        ci = _CI(self.UNITTEST, 'x', URL_BAD_SHA256, 'sha256')
        self.assertFalse(self.ref.refresh(ci))

    def test_good_sha256(self):
        ci = _CI(self.UNITTEST, 'x', URL_SHA256, 'sha256', f'{self.TMPDIR}/x')
        self.assertTrue(self.ref.refresh(ci))

    def test_good_md5(self):
        ci = _CI(self.UNITTEST, 'x', URL_MD5, 'md5', f'{self.TMPDIR}/x')
        self.assertTrue(self.ref.refresh(ci))

    def test_missing_checksum(self):
        ci = _CI(self.UNITTEST, 'x', URL_MISSING, 'sha256', None)
        self.assertFalse(self.ref.refresh(ci))

    def test_unknown_check(self):
        ci = _CI(self.UNITTEST, 'x', URL_BAD_SHA256, 'BAD', None)
        self.assertFalse(self.ref.refresh(ci))

    def test_refresh_force(self):
        cr = ClamavRefresh(Namespace(force=True))
        self.assertEqual(3, cr.refresh_all())

    def test_refresh_age(self):
        r = RefreshLog(URL_SHA256)
        r.updated += timedelta(minutes=10)
        self.s.add(r)
        self.s.commit()
        ci = _CI(self.UNITTEST, 'x', URL_SHA256, 'sha256', f'{self.TMPDIR}/x')
        self.assertFalse(self.ref.refresh(ci))

    def test_refresh_digest_match(self):
        r = RefreshLog(URL_MD5, DIGEST_MD5)
        self.s.add(r)
        self.s.commit()
        ci = _CI(self.UNITTEST, 'x', URL_MD5, 'md5', f'{self.TMPDIR}/x')
        self.assertFalse(self.ref.refresh(ci))

    def test_refresh(self):
        self.s.add(RefreshLog(URL_MD5))
        self.s.commit()
        self.assertEqual(3, self.ref.refresh_all())


if __name__ == '__main__':
    unittest.main()
