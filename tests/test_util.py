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
