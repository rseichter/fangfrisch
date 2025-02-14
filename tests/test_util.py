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

import os
import unittest

from fangfrisch.log import log_error
from fangfrisch.log import log_exception
from fangfrisch.log import log_info
from fangfrisch.util import check_integrity
from fangfrisch.util import parse_hr_bytes
from fangfrisch.util import parse_hr_time
from fangfrisch.util import run_command
from tests import FangfrischTest

SAMPLE_DATA = "fangfrisch".encode("utf-8")
SAMPLE_MD5 = "5e46abab8a827e1534af3a64a3d91f00"
SAMPLE_SHA256 = "64ab093d2f42fe686ee229ab50f650752a74975347141f2e8e947a9d059b891a"


class UtilTests(FangfrischTest):

    def test_md5_fail(self):
        i = check_integrity(SAMPLE_DATA, "md5", "a b")
        self.assertFalse(i.ok)
        self.assertIsNotNone(i.data)

    def test_md5_ok(self):
        i = check_integrity(SAMPLE_DATA, "md5", SAMPLE_MD5)
        self.assertTrue(i.ok)
        self.assertIsNone(i.data)

    def test_sha256_fail(self):
        i = check_integrity(SAMPLE_DATA, "sha256", "b c")
        self.assertFalse(i.ok)

    def test_sha256_ok(self):
        i = check_integrity(SAMPLE_DATA, "sha256", SAMPLE_SHA256)
        self.assertTrue(i.ok)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            i = check_integrity(SAMPLE_DATA, "UNKNOWN_ALGO", "")
            self.assertFalse(i.ok)

    def test_parse_bytes(self):
        self.assertEqual(123, parse_hr_bytes("123"))

    def test_parse_bytes_bad(self):
        self.assertTrue(parse_hr_bytes("BAD") < 0)

    def test_parse_bytes_k(self):
        self.assertEqual(30000, parse_hr_bytes("30k"))

    def test_parse_bytes_mb(self):
        self.assertEqual(2 * 1024 * 1024, parse_hr_bytes("2MB"))

    def test_parse_time(self):
        self.assertEqual(123, parse_hr_time("123m"))

    def test_parse_time_bad(self):
        self.assertTrue(parse_hr_time("321") < 0)

    def test_parse_time_d(self):
        self.assertEqual(24 * 60 * 3, parse_hr_time("3d"))

    def test_parse_time_h(self):
        self.assertEqual(48 * 60, parse_hr_time("48h"))

    def test_run_echo(self):
        self.assertEqual(0, run_command("echo > {path}", 3, log_info, log_error, log_exception, path=os.devnull))

    def test_run_unknown(self):
        self.assertTrue(0 < run_command(self.UNKNOWN, 3, log_info, log_error, log_exception))

    def test_run_timeout(self):
        self.assertNotEqual(0, run_command("sleep 3", 1, log_info, log_error, log_exception))


if __name__ == "__main__":
    unittest.main()
