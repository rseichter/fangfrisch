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

from fangfrisch.config import DB_URL
from fangfrisch.config import ENABLED
from fangfrisch.config import INTEGRITY_CHECK
from fangfrisch.config import LOCAL_DIR
from fangfrisch.config import MAX_AGE
from fangfrisch.config.sanesecurity import sanesecurity
from fangfrisch.config.securiteinfo import securiteinfo
from fangfrisch.config.urlhaus import urlhaus

config_defaults = {
    ENABLED: 'no',
    INTEGRITY_CHECK: 'sha256',
    LOCAL_DIR: '/tmp/fangfrisch',
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

    def dump(self):  # pragma: no cover
        self.parser.write(sys.stdout)

    def get(self, section: str, option: str, fallback=None):
        return self.parser.get(section, option, fallback=fallback)

    def db_url(self):
        return self.parser.get(configparser.DEFAULTSECT, DB_URL, fallback=None)

    def on_update_exec(self):
        return self.parser.get(configparser.DEFAULTSECT, 'on_update_exec', fallback=None)

    def on_update_timeout(self, fallback='30'):
        return self.parser.get(configparser.DEFAULTSECT, 'on_update_timeout', fallback=fallback)

    def is_enabled(self, section: str, fallback=False) -> bool:
        return self.parser.getboolean(section, ENABLED, fallback=fallback)

    def max_age(self, section: str, fallback=1440):
        return self.parser.getint(section, MAX_AGE, fallback=fallback)

    def integrity_check(self, section: str, fallback=None):
        check: str = self.parser.get(section, INTEGRITY_CHECK, fallback=fallback)
        if check and check.lower() in ['disabled', 'no', 'off']:
            return None
        return check

    def local_dir(self, section: str, fallback='.'):
        return self.parser.get(section, LOCAL_DIR, fallback=fallback)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
