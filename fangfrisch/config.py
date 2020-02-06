import configparser, sys

BASE_URL = 'base_url'
SANESECURITY = 'sanesecurity'

_default_config = {
    SANESECURITY: {
        BASE_URL: 'http://ftp.swin.edu.au/sanesecurity/',
        'url_badmacro': 'badmacro.ndb',
        'url_bofhland_cracked': 'bofhland_cracked_URL.ndb',
    }
}


class Configuration:
    parser = None

    def init(self, filename: str = None) -> bool:
        self.parser = configparser.ConfigParser()
        self.parser.read_dict(_default_config)
        if filename:
            parsed = self.parser.read([filename])
            x = len(parsed)
            return x == 1
        return True

    def dump(self):
        self.parser.write(sys.stdout)

    def get(self, section, option, fallback=None):
        return self.parser.get(section, option, fallback=fallback)


config = Configuration()  # Application-level configuration object
