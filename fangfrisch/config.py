import configparser
import sys
from logging import DEBUG

BASE_URL = 'base_url'
MAX_AGE = 'max_age'
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
        MAX_AGE: '1440',  # Minutes in 24h
        'url_badmacro': 'badmacro.ndb',
        'url_blurl': 'blurl.ndb',
        'url_bofhland_cracked_url': 'bofhland_cracked_URL.ndb',
        'url_bofhland_malware_url': 'bofhland_malware_URL.ndb',
        'url_bofhland_malware_attach': 'bofhland_malware_attach.hdb',
        'url_bofhland_phishing_url': 'bofhland_phishing_URL.ndb',
        'url_crdfam.clamav': 'crdfam.clamav.hdb',
        'url_doppelstern-phishtank': 'doppelstern-phishtank.ndb',
        'url_doppelstern_hdb': 'doppelstern.hdb',
        'url_doppelstern': 'doppelstern.ndb',
        'url_foxhole_all_cdb': 'foxhole_all.cdb',
        'url_foxhole_all': 'foxhole_all.ndb',
        'url_foxhole_filename': 'foxhole_filename.cdb',
        'url_foxhole_generic': 'foxhole_generic.cdb',
        'url_foxhole_js_cdb': 'foxhole_js.cdb',
        'url_foxhole_js': 'foxhole_js.ndb',
        'url_foxhole_mail': 'foxhole_mail.cdb',
        'url_junk': 'junk.ndb',
        'url_jurlbl': 'jurlbl.ndb',
        'url_jurlbla': 'jurlbla.ndb',
        'url_lott': 'lott.ndb',
        'url_malware.expert_ndb': 'malware.expert.hdb',
        'url_malware.expert': 'malware.expert.ndb',
        'url_phish': 'phish.ndb',
        'url_phishtank': 'phishtank.ndb',
        'url_porcupine': 'porcupine.ndb',
        'url_rogue': 'rogue.hdb',
        'url_scam': 'scam.ndb',
        'url_scamnailer': 'scamnailer.ndb',
        'url_spamattach': 'spamattach.hdb',
        'url_spamimg': 'spamimg.hdb',
        'url_spear': 'spear.ndb',
        'url_spearl': 'spearl.ndb',
        'url_winnow.attachments': 'winnow.attachments.hdb',
        'url_winnow_bad_cw': 'winnow_bad_cw.hdb',
        'url_winnow_extended_malware': 'winnow_extended_malware.hdb',
        'url_winnow_extended_malware_links': 'winnow_extended_malware_links.ndb',
        'url_winnow_malware': 'winnow_malware.hdb',
        'url_winnow_malware_links': 'winnow_malware_links.ndb',
        'url_winnow_phish_complete': 'winnow_phish_complete.ndb',
        'url_winnow_phish_complete_url': 'winnow_phish_complete_url.ndb',
        'url_winnow_spam_complete': 'winnow_spam_complete.ndb',
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

    def max_age(self, section: str, fallback=(24 * 60)):
        return self.parser.getint(section, MAX_AGE, fallback=fallback)

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
