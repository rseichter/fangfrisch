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

from fangfrisch.config import INTERVAL
from fangfrisch.config import PREFIX

sanesecurity = {
    # See https://sanesecurity.com/usage/signatures/
    "sanesecurity": {
        INTERVAL: "1h",
        PREFIX: r"http://mirror.seichter.de/sanesecurity/",
        "!url_foxhole_all_cdb": f"${{{PREFIX}}}foxhole_all.cdb",
        "!url_foxhole_all_ndb": f"${{{PREFIX}}}foxhole_all.ndb",
        "!url_foxhole_links": f"${{{PREFIX}}}foxhole_links.ldb",
        "!url_foxhole_mail": f"${{{PREFIX}}}foxhole_mail.cdb",
        "!url_winnow_phish_complete": f"${{{PREFIX}}}winnow_phish_complete.ndb",
        "url_badmacro": f"${{{PREFIX}}}badmacro.ndb",
        "url_blurl": f"${{{PREFIX}}}blurl.ndb",
        "url_bofhland_cracked_url": f"${{{PREFIX}}}bofhland_cracked_URL.ndb",
        "url_bofhland_malware_attach": f"${{{PREFIX}}}bofhland_malware_attach.hdb",
        "url_bofhland_malware_url": f"${{{PREFIX}}}bofhland_malware_URL.ndb",
        "url_bofhland_phishing_url": f"${{{PREFIX}}}bofhland_phishing_URL.ndb",
        "url_foxhole_filename": f"${{{PREFIX}}}foxhole_filename.cdb",
        "url_foxhole_generic": f"${{{PREFIX}}}foxhole_generic.cdb",
        "url_foxhole_js_cdb": f"${{{PREFIX}}}foxhole_js.cdb",
        "url_foxhole_js_ndb": f"${{{PREFIX}}}foxhole_js.ndb",
        "url_hackingteam": f"${{{PREFIX}}}hackingteam.hsb",
        "url_junk": f"${{{PREFIX}}}junk.ndb",
        "url_jurlbl": f"${{{PREFIX}}}jurlbl.ndb",
        "url_jurlbla": f"${{{PREFIX}}}jurlbla.ndb",
        "url_lott": f"${{{PREFIX}}}lott.ndb",
        "url_malwareexpert_fp": f"${{{PREFIX}}}malware.expert.fp",
        "url_malwareexpert_hdb": f"${{{PREFIX}}}malware.expert.hdb",
        "url_malwareexpert_ldb": f"${{{PREFIX}}}malware.expert.ldb",
        "url_malwareexpert_ndb": f"${{{PREFIX}}}malware.expert.ndb",
        "url_malwarehash": f"${{{PREFIX}}}malwarehash.hsb",
        "url_phish": f"${{{PREFIX}}}phish.ndb",
        "url_phishtank": f"${{{PREFIX}}}phishtank.ndb",
        "url_porcupine": f"${{{PREFIX}}}porcupine.ndb",
        "url_rogue": f"${{{PREFIX}}}rogue.hdb",
        "url_scam": f"${{{PREFIX}}}scam.ndb",
        "url_shelter": f"${{{PREFIX}}}shelter.ldb",
        "url_sigwhitelist": f"${{{PREFIX}}}sigwhitelist.ign2",
        "url_spamattach": f"${{{PREFIX}}}spamattach.hdb",
        "url_spamimg": f"${{{PREFIX}}}spamimg.hdb",
        "url_spear": f"${{{PREFIX}}}spear.ndb",
        "url_spearl": f"${{{PREFIX}}}spearl.ndb",
        "url_ssftm": f"${{{PREFIX}}}sanesecurity.ftm",
        "url_winnow_attachments": f"${{{PREFIX}}}winnow.attachments.hdb",
        "url_winnow_bad_cw": f"${{{PREFIX}}}winnow_bad_cw.hdb",
        "url_winnow_extended_malware": f"${{{PREFIX}}}winnow_extended_malware.hdb",
        "url_winnow_extended_malware_links": f"${{{PREFIX}}}winnow_extended_malware_links.ndb",
        "url_winnow_malware": f"${{{PREFIX}}}winnow_malware.hdb",
        "url_winnow_malware_links": f"${{{PREFIX}}}winnow_malware_links.ndb",
        "url_winnow_phish_complete_url": f"${{{PREFIX}}}winnow_phish_complete_url.ndb",
        "url_winnow_spam_complete": f"${{{PREFIX}}}winnow_spam_complete.ndb",
    }
}
