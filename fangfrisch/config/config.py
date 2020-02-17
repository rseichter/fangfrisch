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
import sys
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from typing import Optional

from fangfrisch.config import DB_URL
from fangfrisch.config import ENABLED
from fangfrisch.config import INTEGRITY_CHECK
from fangfrisch.config import LOCAL_DIR
from fangfrisch.config import MAX_AGE
from fangfrisch.config import MAX_SIZE
from fangfrisch.config import ON_UPDATE_EXEC
from fangfrisch.config import ON_UPDATE_TIMEOUT
from fangfrisch.config.sanesecurity import sanesecurity
from fangfrisch.config.securiteinfo import securiteinfo
from fangfrisch.config.urlhaus import urlhaus
from fangfrisch.util import parse_hr_bytes

config_defaults = {
    ENABLED: 'no',
    INTEGRITY_CHECK: 'sha256',
    MAX_AGE: '1d',
    MAX_SIZE: '10MB',
    ON_UPDATE_EXEC: '',
    ON_UPDATE_TIMEOUT: '30',  # Timeout in seconds
}
config_other = [sanesecurity, securiteinfo, urlhaus]


class Configuration:
    parser: configparser.ConfigParser = None

    def init(self, filename: str = None) -> bool:
        self.parser = ConfigParser(defaults=config_defaults, interpolation=ExtendedInterpolation())
        for c in config_other:
            self.parser.read_dict(c)
        if filename:
            parsed = self.parser.read([filename])
            return len(parsed) == 1
        return True

    def dump(self) -> None:  # pragma: no cover
        self.parser.write(sys.stdout)

    def get(self, section: str, option: str, fallback=None) -> Optional[str]:
        return self.parser.get(section, option, fallback=fallback)

    def db_url(self) -> Optional[str]:
        return self.parser.get(configparser.DEFAULTSECT, DB_URL)

    def on_update_exec(self) -> Optional[str]:
        return self.parser.get(configparser.DEFAULTSECT, ON_UPDATE_EXEC)

    def on_update_timeout(self) -> int:
        return self.parser.getint(configparser.DEFAULTSECT, ON_UPDATE_TIMEOUT)

    def is_enabled(self, section: str, fallback=False) -> bool:
        return self.parser.getboolean(section, ENABLED, fallback=fallback)

    def max_age(self, section: str) -> int:
        return self.parser.getint(section, MAX_AGE)

    def max_size(self, section: str) -> int:
        size = self.parser.get(section, MAX_SIZE)
        return parse_hr_bytes(size)

    def integrity_check(self, section: str) -> Optional[str]:
        check: str = self.parser.get(section, INTEGRITY_CHECK)
        if check and check.lower() in ['disabled', 'no', 'off']:
            return None
        return check

    def local_dir(self, section: str, fallback='.') -> str:
        return self.parser.get(section, LOCAL_DIR, fallback=fallback)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
