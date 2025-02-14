"""
Copyright © 2020-2025 Ralph Seichter

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

import tempfile
import unittest
from argparse import Namespace
from datetime import timedelta

from fangfrisch.db import RefreshLog
from fangfrisch.refresh import ClamavRefresh
from fangfrisch.refresh import _is_url_disabled
from tests import DIGEST_DUMMY
from tests import DIGEST_MD5
from tests import FangfrischTest
from tests import NETWORK_TESTS
from tests import URL_BAD_SHA256
from tests import URL_MD5
from tests import URL_MISSING
from tests import URL_SHA256
from tests import _ClamavTestItem


class RefreshTests(FangfrischTest):
    ref = ClamavRefresh(Namespace(force=False))

    def setUp(self) -> None:
        super().setUp()
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.commit()

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_404(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_BAD_SHA256 + "BAD")
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_bad_sha256(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_BAD_SHA256, "sha256")
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_good_sha256(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_SHA256, "sha256", f"{self.TMPDIR}/x")
        self.assertTrue(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_good_md5(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_MD5, "md5", f"{self.TMPDIR}/x")
        self.assertTrue(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_missing_checksum(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_MISSING, "sha256")
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_missing_path(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_MD5, "md5")
        with self.assertRaises(TypeError):
            self.assertTrue(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_unknown_check(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_BAD_SHA256, "BAD")
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_refresh_force(self):
        cr = ClamavRefresh(Namespace(force=True))
        (n, t) = cr.refresh_all()
        self.assertEqual(3, n)
        self.assertEqual(2, t)

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_refresh_age(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_SHA256, "sha256", f"{self.TMPDIR}/x")
        r = RefreshLog(ci, DIGEST_DUMMY)
        r.updated += timedelta(minutes=10)
        self.s.add(r)
        self.s.commit()
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_refresh_digest_match(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_MD5, "md5", f"{self.TMPDIR}/x")
        r = RefreshLog(ci, DIGEST_MD5)
        self.s.add(r)
        self.s.commit()
        self.assertFalse(self.ref.refresh(ci))

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_refresh(self):
        ci = _ClamavTestItem(self.UNITTEST, "x", URL_MD5, "md5", f"{self.TMPDIR}/x")
        self.s.add(RefreshLog(ci, DIGEST_DUMMY))
        self.s.commit()
        (n, t) = self.ref.refresh_all()
        self.assertEqual(3, n)
        self.assertEqual(2, t)

    @unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
    def test_url_blank(self):
        ci = _ClamavTestItem("unittest4", "url_blank", "", "md5", f"{self.TMPDIR}/blank")
        self.s.add(RefreshLog(ci, DIGEST_DUMMY))
        self.s.commit()
        (n, t) = self.ref.refresh_all()
        self.assertEqual(3, n)
        self.assertEqual(3, n)

    def test_url_disabled(self):
        self.assertTrue(_is_url_disabled(None))
        self.assertTrue(_is_url_disabled(" "))
        self.assertTrue(_is_url_disabled("Disabled"))

    def test_print_mappings(self):
        file = tempfile.TemporaryFile(mode="w+t")
        ClamavRefresh.print_url_path_mappings(file)
        file.seek(0)
        data = file.read()
        self.assertTrue(data.startswith("unittest\t"))
        file.close()


if __name__ == "__main__":
    unittest.main()
