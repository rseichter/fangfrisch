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

from fangfrisch.db import RefreshLog
from fangfrisch.dump import DumpDbEntries
from fangfrisch.refresh import ClamavRefresh
from tests import FangfrischTest
from tests import _ClamavTestItem


class DumpDbTests(FangfrischTest):
    ref = ClamavRefresh(Namespace(force=False))

    def setUp(self) -> None:
        super().setUp()
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        cia = _ClamavTestItem("spam", "option", "a", path="a")
        cib = _ClamavTestItem("spamalot", "option", "b", path="b")
        self.s.add(RefreshLog(cia, "dummy"))
        self.s.add(RefreshLog(cib, "dummy"))
        self.s.commit()
        self.s.commit()

    def test_dump_all(self):
        file = tempfile.TemporaryFile(mode="w+t")
        dump = DumpDbEntries(Namespace(provider="."))
        dump.print_url_path_mappings(file)
        file.seek(0)
        data = file.read()
        file.close()
        self.assertTrue(data.startswith("spam"))

    def test_match_two(self):
        x = RefreshLog.url_path_mappings("spam")
        self.assertEqual(2, len(x))

    def test_match_one(self):
        x = RefreshLog.url_path_mappings("^spam$")
        self.assertEqual(1, len(x))

    def test_match_none(self):
        x = RefreshLog.url_path_mappings("ham")
        self.assertEqual(0, len(x))


if __name__ == "__main__":
    unittest.main()
