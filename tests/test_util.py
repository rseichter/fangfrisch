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


if __name__ == '__main__':
    unittest.main()
