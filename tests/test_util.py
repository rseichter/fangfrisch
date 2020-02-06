import os
import unittest
import uuid

from fangfrisch.util import check_sha256
from fangfrisch.util import write_binary
from tests import FangfrischTest

SAMPLE_DATA = 'fangfrisch'.encode('utf-8')
SAMPLE_DIGEST = '64ab093d2f42fe686ee229ab50f650752a74975347141f2e8e947a9d059b891a'
UNIQUE = uuid.uuid4().hex


class UtilTests(FangfrischTest):

    def test_sha256_fail(self):
        self.assertFalse(check_sha256(SAMPLE_DATA, 'a b'))

    def test_sha256_ok(self):
        self.assertTrue(check_sha256(SAMPLE_DATA, SAMPLE_DIGEST))

    def test_write_fail(self):
        with self.assertRaises(OSError):
            f = os.path.join('/', UNIQUE)
            write_binary(SAMPLE_DATA, f)

    def test_write_ok(self):
        f = os.path.join(self.TMPDIR, UNIQUE)
        self.assertTrue(write_binary(SAMPLE_DATA, f))


if __name__ == '__main__':
    unittest.main()
