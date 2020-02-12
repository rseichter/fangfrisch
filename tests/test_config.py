import unittest

from fangfrisch.config import BASE_URL
from fangfrisch.config.config import Configuration
from tests import FangfrischTest

SECTION = 'sanesecurity'


class ConfigTests(FangfrischTest):
    c: Configuration = None

    def setUp(self) -> None:
        self.c = Configuration()

    def test_sanesec_base_url(self):
        self.c.init()
        self.assertIsNotNone(self.c.get(SECTION, BASE_URL))

    def test_sanesec_unknown(self):
        self.c.init()
        self.assertIsNone(self.c.get(SECTION, self.UNKNOWN))

    def test_unknown_section(self):
        self.c.init()
        self.assertIsNone(self.c.get(self.UNKNOWN, BASE_URL))

    def test_missing_file(self):
        self.assertFalse(self.c.init(self.UNKNOWN))

    def test_combined_url(self):
        self.c.init(self.CONF)
        self.assertEqual('http://ftp.swin.edu.au/sanesecurity/badmacro.ndb',
                         self.c.base_url(SECTION) + self.c.get(SECTION, 'url_badmacro'))

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
