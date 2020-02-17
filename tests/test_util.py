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

from fangfrisch.util import check_integrity
from fangfrisch.util import parse_hr_bytes, parse_hr_time
from tests import FangfrischTest

SAMPLE_DATA = 'fangfrisch'.encode('utf-8')
SAMPLE_MD5 = '5e46abab8a827e1534af3a64a3d91f00'
SAMPLE_SHA256 = '64ab093d2f42fe686ee229ab50f650752a74975347141f2e8e947a9d059b891a'


class UtilTests(FangfrischTest):

    def test_md5_fail(self):
        status, msg = check_integrity(SAMPLE_DATA, 'md5', 'a b')
        self.assertFalse(status)
        self.assertIsNotNone(msg)

    def test_md5_ok(self):
        status, msg = check_integrity(SAMPLE_DATA, 'md5', SAMPLE_MD5)
        self.assertTrue(status)
        self.assertIsNone(msg)

    def test_sha256_fail(self):
        status, msg = check_integrity(SAMPLE_DATA, 'sha256', 'b c')
        self.assertFalse(status)

    def test_sha256_ok(self):
        status, msg = check_integrity(SAMPLE_DATA, 'sha256', SAMPLE_SHA256)
        self.assertTrue(status)

    def test_unknown(self):
        with self.assertRaises(ValueError):
            status, msg = check_integrity(SAMPLE_DATA, 'UNKNOWN_ALGO', '')
            self.assertFalse(status)

    def test_parse_bytes(self):
        self.assertEqual(123, parse_hr_bytes('123'))

    def test_parse_bytes_bad(self):
        self.assertTrue(parse_hr_bytes('BAD') < 0)

    def test_parse_bytes_k(self):
        self.assertEqual(30000, parse_hr_bytes('30k'))

    def test_parse_bytes_mb(self):
        self.assertEqual(2 * 1024 * 1024, parse_hr_bytes('2MB'))

    def test_parse_time(self):
        self.assertEqual(123, parse_hr_time('123m'))

    def test_parse_time_bad(self):
        self.assertTrue(parse_hr_time('321') < 0)

    def test_parse_time_d(self):
        self.assertEqual(24 * 60 * 3, parse_hr_time('3d'))

    def test_parse_time_h(self):
        self.assertEqual(48 * 60, parse_hr_time('48h'))


if __name__ == '__main__':
    unittest.main()
