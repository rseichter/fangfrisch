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

from sqlalchemy.exc import IntegrityError

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from tests import DIGEST_DUMMY
from tests import FangfrischTest
from tests import _ClamavTestItem

URL1 = 'https://u1'
URL2 = 'https://u2'
config.init(FangfrischTest.CONF)


class DbTests(FangfrischTest):
    s = None

    def setUp(self) -> None:
        super().setUp()
        self.ci = _ClamavTestItem(url=URL1, section=self.UNITTEST, option='option', path='path')
        RefreshLog.init(create_all=True)
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        self.s.commit()

    def test_duplicate(self):
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        with self.assertRaises(IntegrityError):
            self.s.commit()

    def test_missing_path(self):
        self.ci.path = None
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        with self.assertRaises(IntegrityError):
            self.s.commit()

    def test_insert(self):
        self.ci.url = URL2
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        self.s.commit()
        self.assertTrue(True)  # Must not raise an exception

    def test_refresh_required(self):
        self.assertTrue(RefreshLog.is_outdated(URL1, 0))

    def test_stamp1(self):
        RefreshLog.update(self.ci, DIGEST_DUMMY)  # Must not raise an exception
        self.assertTrue(True)

    def test_stamp2(self):
        self.ci.url = URL2
        RefreshLog.update(self.ci, DIGEST_DUMMY)  # Must not raise an exception
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
