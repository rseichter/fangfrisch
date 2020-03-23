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
from fangfrisch.config import MAX_SIZE
from fangfrisch.config.malwarepatrol import malwarepatrol
from fangfrisch.config.sanesecurity import sanesecurity
from fangfrisch.config.securiteinfo import securiteinfo
from fangfrisch.config.urlhaus import urlhaus
from fangfrisch.util import parse_hr_bytes
from fangfrisch.util import parse_hr_time


def means_automatic(s: Optional[str]) -> bool:
    return s and s.lower() in ['auto', 'automatic', 'default']


def means_disabled(s: Optional[str]) -> bool:
    return s and s.lower() in ['disabled', 'false', 'no', 'off']


class Configuration:
    parser: configparser.ConfigParser = None

    def init(self, filename: str = None) -> bool:
        defaults = {
            CLEANUP: 'automatic',
            ENABLED: 'false',
            INTEGRITY_CHECK: 'sha256',
            MAX_SIZE: '10MB',
        }
        self.parser = ConfigParser(defaults=defaults, interpolation=ExtendedInterpolation())
        for c in [malwarepatrol, sanesecurity, securiteinfo, urlhaus]:
            self.parser.read_dict(c)
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
        return means_automatic(self.parser.get(section, CLEANUP))

    def db_url(self) -> Optional[str]:
        return self.parser.get(configparser.DEFAULTSECT, DB_URL)

    def on_update_exec(self, fallback='') -> str:
        return self.parser.get(configparser.DEFAULTSECT, 'on_update_exec', fallback=fallback)

    def on_update_timeout(self, fallback=30) -> int:
        return self.parser.getint(configparser.DEFAULTSECT, 'on_update_timeout', fallback=fallback)

    def is_enabled(self, section: str, fallback=False) -> bool:
        return self.parser.getboolean(section, ENABLED, fallback=fallback)

    def interval(self, section: str, fallback='') -> int:
        age = self.parser.get(section, INTERVAL, fallback=fallback)
        return parse_hr_time(age)

    def max_size(self, section: str) -> int:
        size = self.parser.get(section, MAX_SIZE)
        return parse_hr_bytes(size)

    def integrity_check(self, section: str) -> Optional[str]:
        check: str = self.parser.get(section, INTEGRITY_CHECK)
        if means_disabled(check):
            return None
        return check

    def local_dir(self, section: str, fallback='') -> str:
        return self.parser.get(section, LOCAL_DIR, fallback=fallback)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
