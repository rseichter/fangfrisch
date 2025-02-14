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
import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from fangfrisch.db import DbMeta
from fangfrisch.db import RefreshLog
from tests import DIGEST_DUMMY
from tests import FangfrischTest
from tests import _ClamavTestItem

URL1 = "https://u1"
URL2 = "https://u2"


class DbTests(FangfrischTest):
    s = None

    def setUp(self) -> None:
        super().setUp()
        self.ci = _ClamavTestItem(url=URL1, section=self.UNITTEST, option="option", path="path")
        RefreshLog.init()
        self.s = RefreshLog._session()
        self.s.query(RefreshLog).delete()
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        self.s.commit()

    def test_version_match(self):
        self.assertTrue(DbMeta.assert_version_match())

    def test_version_mismatch(self):
        session = DbMeta._session()
        dm: DbMeta = session.query(DbMeta).one()
        dm.db_version = -1
        session.add(dm)
        session.commit()
        with self.assertRaises(SystemExit):
            DbMeta.assert_version_match()

    def test_version_missing(self):
        session = DbMeta._session()
        session.query(DbMeta).delete()
        session.commit()
        with self.assertRaises(NoResultFound):
            DbMeta.assert_version_match()

    def test_create_metadata1(self):
        session = DbMeta._session()
        session.query(DbMeta).delete()
        session.commit()
        self.assertTrue(DbMeta().create_metadata(False))

    def test_create_metadata2(self):
        with self.assertRaises(SystemExit):
            DbMeta().create_metadata(False)

    def test_create_metadata3(self):
        self.assertTrue(DbMeta().create_metadata(True))

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

    def test_cleanup1(self):
        self.assertEqual(0, RefreshLog.cleanup_provider(self.UNKNOWN))

    def test_cleanup2(self):
        file = tempfile.NamedTemporaryFile(mode="w+t", encoding="utf-8", delete=False)
        file.write(self.UNITTEST)
        file.close()
        provider = uuid.uuid4().hex
        self.ci.section = provider
        self.ci.path = file.name
        self.ci.url = URL2
        self.s.add(RefreshLog(self.ci, DIGEST_DUMMY))
        self.s.commit()
        self.assertEqual(1, RefreshLog.cleanup_provider(provider))


if __name__ == "__main__":
    unittest.main()
