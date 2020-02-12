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

from fangfrisch.util import check_sha256
from tests import FangfrischTest

SAMPLE_DATA = 'fangfrisch'.encode('utf-8')
SAMPLE_DIGEST = '64ab093d2f42fe686ee229ab50f650752a74975347141f2e8e947a9d059b891a'


class UtilTests(FangfrischTest):

    def test_sha256_fail(self):
        self.assertFalse(check_sha256(SAMPLE_DATA, 'a b'))

    def test_sha256_ok(self):
        self.assertTrue(check_sha256(SAMPLE_DATA, SAMPLE_DIGEST))


if __name__ == '__main__':
    unittest.main()
