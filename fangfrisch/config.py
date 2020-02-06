import configparser
import sys
from logging import DEBUG

BASE_URL = 'base_url'
INTEGRITY_CHECK = 'integrity_check'
SANESECURITY = 'sanesecurity'
LOCAL_DIR = 'local_directory'

defaults = {
    INTEGRITY_CHECK: 'sha256',
    LOCAL_DIR: '/tmp/fangfrisch',
}

sections = {
    SANESECURITY: {
        BASE_URL: 'http://ftp.swin.edu.au/sanesecurity/',
        'url_badmacro': 'badmacro.ndb',
        'url_bofhland_cracked': 'bofhland_cracked_URL.ndb',
    }
}


class Configuration:
    parser: configparser.ConfigParser = None

    def init(self, filename: str = None) -> bool:
        self.parser = configparser.ConfigParser(defaults=defaults)
        self.parser.read_dict(sections)
        if filename:
            parsed = self.parser.read([filename])
            x = len(parsed)
            return x == 1
        return True

    def dump(self):  # pragma: no cover
        self.parser.write(sys.stdout)

    def get(self, section: str, option: str, fallback=None):
        return self.parser.get(section, option, fallback=fallback)

    def base_url(self, section: str, fallback=None):
        return self.parser.get(section, BASE_URL, fallback=fallback)

    def integrity_check(self, section: str, fallback=None):
        return self.parser.get(section, INTEGRITY_CHECK, fallback=fallback)

    def log_level(self):
        return self.parser.get('DEFAULT', 'log_level', fallback=DEBUG)

    def local_dir(self, section: str):
        return self.parser.get(section, LOCAL_DIR)

    def options(self, section: str):
        return self.parser.options(section)

    def sections(self):
        return self.parser.sections()


config = Configuration()  # Application-level configuration object
