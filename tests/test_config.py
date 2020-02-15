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

from fangfrisch.config import PREFIX
from fangfrisch.config.config import Configuration
from tests import FangfrischTest

SECTION = 'sanesecurity'


class ConfigTests(FangfrischTest):
    c: Configuration = None

    def setUp(self) -> None:
        self.c = Configuration()

    def test_sanesec_base_url(self):
        self.c.init()
        self.assertIsNotNone(self.c.get(SECTION, PREFIX))

    def test_sanesec_unknown(self):
        self.c.init()
        self.assertIsNone(self.c.get(SECTION, self.UNKNOWN))

    def test_unknown_section(self):
        self.c.init()
        self.assertIsNone(self.c.get(self.UNKNOWN, PREFIX))

    def test_missing_file(self):
        self.assertFalse(self.c.init(self.UNKNOWN))

    def test_local_dir(self):
        self.c.init(self.CONF)
        self.assertEqual(self.TMPDIR, self.c.local_dir(self.UNITTEST))

    def test_integrity_check(self):
        self.c.init(self.CONF)
        self.assertEqual('sha256', self.c.integrity_check(self.UNITTEST))

    def test_sections(self):
        self.c.init(self.CONF)
        s = self.c.sections()
        self.assertIn(self.UNITTEST, s)

    def test_max_age(self):
        self.c.init(self.CONF)
        self.assertEqual(60 * 24, self.c.max_age(SECTION))


if __name__ == '__main__':
    unittest.main()
