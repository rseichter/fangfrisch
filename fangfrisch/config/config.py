import configparser
import sys

from fangfrisch.config import BASE_URL
from fangfrisch.config import DB_URL
from fangfrisch.config import ENABLED
from fangfrisch.config import MAX_AGE
from fangfrisch.config.sanesecurity import _config_sanesecurity

INTEGRITY_CHECK = 'integrity_check'
LOCAL_DIR = 'local_directory'

_config_defaults = {
    ENABLED: '0',
    INTEGRITY_CHECK: 'sha256',
    LOCAL_DIR: '/tmp/fangfrisch',
}
_config_other = [_config_sanesecurity]


class Configuration:
    parser: configparser.ConfigParser = None

    def init(self, filename: str = None) -> bool:
        self.parser = configparser.ConfigParser(defaults=_config_defaults)
        for c in _config_other:
            self.parser.read_dict(c)
        if filename:
            parsed = self.parser.read([filename])
            return len(parsed) == 1
        return True

    def dump(self):  # pragma: no cover
        self.parser.write(sys.stdout)

    def get(self, section: str, option: str, fallback=None):
        return self.parser.get(section, option, fallback=fallback)

    def base_url(self, section: str, fallback=None):
        return self.parser.get(section, BASE_URL, fallback=fallback)

    def db_url(self):
        return self.parser.get(configparser.DEFAULTSECT, DB_URL, fallback=None)

    def is_enabled(self, section: str, fallback=False) -> bool:
        return self.parser.getboolean(section, ENABLED, fallback=fallback)

    def max_age(self, section: str, fallback=(24 * 60)):
        return self.parser.getint(section, MAX_AGE, fallback=fallback)

    def integrity_check(self, section: str, fallback=None):
        check: str = self.parser.get(section, INTEGRITY_CHECK, fallback=fallback)
        if check and check.lower() in ['disabled', 'no', 'off']:
            return None
        return check

    def local_dir(self, section: str):
        return self.parser.get(section, LOCAL_DIR)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
