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

import os
import unittest
import uuid

import fangfrisch.log
from fangfrisch import ClamavItem
from fangfrisch.config.config import config
from fangfrisch.db import DbMeta
from fangfrisch.log import LogHandlerType
from fangfrisch.log import init_logger

DIGEST_DUMMY = "digest_dummy"
DIGEST_MD5 = "6087a61850f22a132f8522f35779c04d"
MAX_SIZE = 1024 * 1024
PATH_DUMMY = "path_dummy"
URL_BAD_SHA256 = "https://seichter.de/favicon.ico"
URL_MD5 = "https://seichter.de/favicon-32x32.png"
URL_MISSING = "https://seichter.de/index.html"
URL_SHA256 = "https://seichter.de/favicon-16x16.png"


def env_var(name: str, default: object = None):
    if name in os.environ:
        return os.environ[name]
    return default


NETWORK_TESTS = env_var("NETWORK_TESTS") == "1"


class _ClamavTestItem(ClamavItem):
    def __init__(
        self,
        section,
        option,
        url,
        check=None,
        path=None,
        interval=0,
        max_size=MAX_SIZE,
        on_update=None,
        connection_timeout=10,
        stem="test_item",
    ) -> None:
        super().__init__(
            check=check,
            connection_timeout=connection_timeout,
            interval=interval,
            max_size=max_size,
            on_update=on_update,
            option=option,
            path=path,
            section=section,
            stem=stem,
            url=url,
        )


class FangfrischTest(unittest.TestCase):
    CONF = "tests/tests.conf"
    TMPDIR = "/tmp/fangfrisch/unittest"
    UNITTEST = "unittest"
    UNKNOWN = uuid.uuid4().hex

    @classmethod
    def setUpClass(cls) -> None:
        config.init(FangfrischTest.CONF)
        os.makedirs(FangfrischTest.TMPDIR, exist_ok=True)
        if fangfrisch.log._handler is not None:
            fangfrisch.log._handler.close()
            fangfrisch.log._handler = None
        init_logger(LogHandlerType.CONSOLE, "FATAL", "")
        DbMeta.init(True)
