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

import unittest

# noinspection PyProtectedMember
from fangfrisch.download import _download
from tests import FangfrischTest
from tests import MAX_SIZE
from tests import NETWORK_TESTS
from tests import URL_SHA256


@unittest.skipUnless(NETWORK_TESTS, "network tests disabled")
class DownloadTests(FangfrischTest):
    def test_get_ok(self):
        d = _download(URL_SHA256, MAX_SIZE, 10)
        self.assertTrue(d.ok)

    def test_get_oversized(self):
        d = _download(URL_SHA256, 1, 10)
        self.assertFalse(d.ok)


if __name__ == "__main__":
    unittest.main()
