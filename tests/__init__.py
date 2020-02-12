import logging
import os
import unittest
import uuid

from fangfrisch.logging import log


def to_bool(x: str) -> bool:
    return x and x.lower() in ['1', 'enabled', 'y', 'yes', 'true']


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
        return to_bool(os.getenv('RUN_ONLINE_TESTS', '0'))
