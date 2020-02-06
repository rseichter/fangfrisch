import unittest
import uuid

from fangfrisch.config import BASE_URL
from fangfrisch.config import Configuration
from fangfrisch.config import SANESECURITY

UNKNOWN = uuid.uuid4().hex


class ConfigTests(unittest.TestCase):
    c: Configuration = None

    def setUp(self) -> None:
        self.c = Configuration()

    def test_sanesec_base_url(self):
        self.c.init()
        self.assertIsNotNone(self.c.get(SANESECURITY, BASE_URL))

    def test_sanesec_unknown(self):
        self.c.init()
        self.assertIsNone(self.c.get(SANESECURITY, UNKNOWN))

    def test_unknown_section(self):
        self.c.init()
        self.assertIsNone(self.c.get(UNKNOWN, BASE_URL))

    def test_missing_file(self):
        self.assertFalse(self.c.init(UNKNOWN))


if __name__ == '__main__':
    unittest.main()
