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

from sqlalchemy.exc import IntegrityError

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from tests import FangfrischTest

ID1 = 'test_1'
ID2 = 'test_2'

config.init(FangfrischTest.CONF)


class DbTests(FangfrischTest):
    s = None

    def setUp(self) -> None:
        super().setUp()
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.add(RefreshLog(ID1))
        self.s.commit()

    def test_duplicate(self):
        self.s.add(RefreshLog(ID1))
        with self.assertRaises(IntegrityError):
            self.s.commit()

    def test_insert(self):
        self.s.add(RefreshLog(ID2))
        self.s.commit()
        self.assertTrue(True)  # Must not raise an exception

    def test_refresh_required(self):
        self.assertTrue(RefreshLog.refresh_required(ID1, 0))

    def test_stamp1(self):
        RefreshLog.stamp_by_url(ID1)  # Must not raise an exception
        self.assertTrue(True)

    def test_stamp2(self):
        RefreshLog.stamp_by_url(ID2)  # Must not raise an exception
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
