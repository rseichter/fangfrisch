import logging
import os
import unittest
import uuid

from fangfrisch.logging import log
from fangfrisch.util import represents_true


class FangfrischTest(unittest.TestCase):
    CONF = 'tests/tests.conf'
    TMPDIR = f'/tmp/fangfrisch/unittest'
    UNITTEST = 'unittest'
    UNKNOWN = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls) -> None:
        log.setLevel(logging.FATAL)

    @classmethod
    def online_tests(cls):
        return represents_true(os.getenv('RUN_ONLINE_TESTS', '0'))
