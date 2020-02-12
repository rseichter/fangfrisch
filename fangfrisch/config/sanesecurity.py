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
along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
from fangfrisch.config import MAX_AGE
from fangfrisch.config import PREFIX

sanesecurity = {
    'sanesecurity': {
        MAX_AGE: str(24 * 60),  # Max age in minutes
        PREFIX: 'http://ftp.swin.edu.au/sanesecurity/',
        'url_badmacro': f'${{{PREFIX}}}badmacro.ndb',
        'url_blurl': f'${{{PREFIX}}}blurl.ndb',
        'url_bofhland_cracked_url': f'${{{PREFIX}}}bofhland_cracked_URL.ndb',
        'url_bofhland_malware_attach': f'${{{PREFIX}}}bofhland_malware_attach.hdb',
        'url_bofhland_malware_url': f'${{{PREFIX}}}bofhland_malware_URL.ndb',
        'url_bofhland_phishing_url': f'${{{PREFIX}}}bofhland_phishing_URL.ndb',
        'url_crdfam_clamav': f'${{{PREFIX}}}crdfam.clamav.hdb',
        'url_doppelstern': f'${{{PREFIX}}}doppelstern.ndb',
        'url_doppelstern-phishtank': f'${{{PREFIX}}}doppelstern-phishtank.ndb',
        'url_doppelstern_hdb': f'${{{PREFIX}}}doppelstern.hdb',
        'url_foxhole_all': f'${{{PREFIX}}}foxhole_all.ndb',
        'url_foxhole_all_cdb': f'${{{PREFIX}}}foxhole_all.cdb',
        'url_foxhole_filename': f'${{{PREFIX}}}foxhole_filename.cdb',
        'url_foxhole_generic': f'${{{PREFIX}}}foxhole_generic.cdb',
        'url_foxhole_js': f'${{{PREFIX}}}foxhole_js.ndb',
        'url_foxhole_js_cdb': f'${{{PREFIX}}}foxhole_js.cdb',
        'url_foxhole_mail': f'${{{PREFIX}}}foxhole_mail.cdb',
        'url_junk': f'${{{PREFIX}}}junk.ndb',
        'url_jurlbl': f'${{{PREFIX}}}jurlbl.ndb',
        'url_jurlbla': f'${{{PREFIX}}}jurlbla.ndb',
        'url_lott': f'${{{PREFIX}}}lott.ndb',
        'url_malware.expert': f'${{{PREFIX}}}malware.expert.ndb',
        'url_malware.expert_ndb': f'${{{PREFIX}}}malware.expert.hdb',
        'url_phish': f'${{{PREFIX}}}phish.ndb',
        'url_phishtank': f'${{{PREFIX}}}phishtank.ndb',
        'url_porcupine': f'${{{PREFIX}}}porcupine.ndb',
        'url_rogue': f'${{{PREFIX}}}rogue.hdb',
        'url_scam': f'${{{PREFIX}}}scam.ndb',
        'url_scamnailer': f'${{{PREFIX}}}scamnailer.ndb',
        'url_spamattach': f'${{{PREFIX}}}spamattach.hdb',
        'url_spamimg': f'${{{PREFIX}}}spamimg.hdb',
        'url_spear': f'${{{PREFIX}}}spear.ndb',
        'url_spearl': f'${{{PREFIX}}}spearl.ndb',
        'url_winnow_attachments': f'${{{PREFIX}}}winnow.attachments.hdb',
        'url_winnow_bad_cw': f'${{{PREFIX}}}winnow_bad_cw.hdb',
        'url_winnow_extended_malware': f'${{{PREFIX}}}winnow_extended_malware.hdb',
        'url_winnow_extended_malware_links': f'${{{PREFIX}}}winnow_extended_malware_links.ndb',
        'url_winnow_malware': f'${{{PREFIX}}}winnow_malware.hdb',
        'url_winnow_malware_links': f'${{{PREFIX}}}winnow_malware_links.ndb',
        'url_winnow_phish_complete': f'${{{PREFIX}}}winnow_phish_complete.ndb',
        'url_winnow_phish_complete_url': f'${{{PREFIX}}}winnow_phish_complete_url.ndb',
        'url_winnow_spam_complete': f'${{{PREFIX}}}winnow_spam_complete.ndb',
    }
}
