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
import logging
import unittest
import uuid

from fangfrisch.logging import log

DIGEST_MD5 = '6087a61850f22a132f8522f35779c04d'
MAX_SIZE = 1024 * 1024
URL_BAD_SHA256 = 'https://seichter.de/favicon.ico'
URL_MD5 = 'https://seichter.de/favicon-32x32.png'
URL_MISSING = 'https://seichter.de/index.html'
URL_SHA256 = 'https://seichter.de/favicon-16x16.png'


def to_bool(x: str) -> bool:
    return x and x.lower() in ['1', 'enabled', 'y', 'yes', 'true']


class FangfrischTest(unittest.TestCase):
    CONF = 'tests/tests.conf'
    TMPDIR = f'/tmp/fangfrisch/unittest'
    UNITTEST = 'unittest'
    UNKNOWN = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls) -> None:
        log.setLevel(logging.ERROR)
