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

import configparser
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from typing import Optional

from fangfrisch.config import CLEANUP
from fangfrisch.config import DB_URL
from fangfrisch.config import ENABLED
from fangfrisch.config import INTEGRITY_CHECK
from fangfrisch.config import INTERVAL
from fangfrisch.config import LOCAL_DIR
from fangfrisch.config import LOG_FORMAT
from fangfrisch.config import LOG_LEVEL
from fangfrisch.config import LOG_METHOD
from fangfrisch.config import LOG_TARGET
from fangfrisch.config import MAX_SIZE
from fangfrisch.config.fangfrischnews import fangfrischnews
from fangfrisch.config.interserver import interserver
from fangfrisch.config.malwarepatrol import malwarepatrol
from fangfrisch.config.sanesecurity import sanesecurity
from fangfrisch.config.securiteinfo import securiteinfo
from fangfrisch.config.urlhaus import urlhaus
from fangfrisch.util import parse_hr_bytes
from fangfrisch.util import parse_hr_time


def means_automatic(s: Optional[str]) -> bool:
    return s and s.lower() in ["auto", "automatic", "default"]


def means_disabled(s: Optional[str]) -> bool:
    return s and s.lower() in ["disabled", "false", "no", "off"]


class Configuration:
    parser: configparser.ConfigParser = None

    def init(self, filename: str = None) -> bool:
        defaults = {
            CLEANUP: "automatic",
            ENABLED: "no",
            INTEGRITY_CHECK: "sha256",
            LOG_LEVEL: "WARNING",
            LOG_METHOD: "console",
            MAX_SIZE: "10MB",
        }
        self.parser = ConfigParser(defaults=defaults, interpolation=ExtendedInterpolation())
        for dict_ in [
            fangfrischnews,
            interserver,
            malwarepatrol,
            sanesecurity,
            securiteinfo,
            urlhaus,
        ]:
            self.parser.read_dict(dict_)
        if filename:
            parsed = self.parser.read([filename])
            return len(parsed) == 1
        return True

    def write(self, file_descriptor) -> bool:
        self.parser.write(file_descriptor)
        return True  # Not reached in case of exceptions

    def get(self, section: str, option: str, fallback=None) -> Optional[str]:
        return self.parser.get(section, option, fallback=fallback)

    def auto_cleanup(self, section: str) -> bool:
        # Default: see init() method
        return means_automatic(self.parser.get(section, CLEANUP))

    def connection_timeout(self, fallback=30) -> int:
        return self.parser.getint(configparser.DEFAULTSECT, "connection_timeout", fallback=fallback)

    def db_url(self) -> Optional[str]:
        # No default
        return self.parser.get(configparser.DEFAULTSECT, DB_URL)

    def on_update_exec(self, section: str = configparser.DEFAULTSECT, fallback="") -> str:
        return self.parser.get(section, "on_update_exec", fallback=fallback)

    def on_update_timeout(self, section: str = configparser.DEFAULTSECT, fallback=30) -> int:
        return self.parser.getint(section, "on_update_timeout", fallback=fallback)

    def is_enabled(self, section: str, fallback=False) -> bool:
        # Default: see init() method
        return self.parser.getboolean(section, ENABLED, fallback=fallback)

    def interval(self, section: str, fallback="") -> int:
        age = self.parser.get(section, INTERVAL, fallback=fallback)
        return parse_hr_time(age)

    def max_size(self, section: str) -> int:
        # Default: see init() method
        return parse_hr_bytes(self.parser.get(section, MAX_SIZE))

    def integrity_check(self, section: str) -> Optional[str]:
        # Default: see init() method
        check: str = self.parser.get(section, INTEGRITY_CHECK)
        if means_disabled(check):
            return None
        return check

    def local_dir(self, section: str, fallback="") -> str:
        return self.parser.get(section, LOCAL_DIR, fallback=fallback)

    def log_format(self, fallback=None) -> Optional[str]:
        return self.parser.get(configparser.DEFAULTSECT, LOG_FORMAT, fallback=fallback)

    def log_level(self) -> str:
        # Default: see init() method
        return self.parser.get(configparser.DEFAULTSECT, LOG_LEVEL).upper()

    def log_method(self) -> str:
        # Default: see init() method
        return self.parser.get(configparser.DEFAULTSECT, LOG_METHOD)

    def log_target(self, fallback="localhost") -> str:
        return self.parser.get(configparser.DEFAULTSECT, LOG_TARGET, fallback=fallback)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
