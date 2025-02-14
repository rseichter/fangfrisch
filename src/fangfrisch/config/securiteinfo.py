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
from fangfrisch.config import MAX_SIZE
from fangfrisch.config import PREFIX

securiteinfo = {
    "securiteinfo": {
        "customer_id": "you_forgot_to_configure_customer_id",
        INTERVAL: "1h",
        MAX_SIZE: "20MB",
        PREFIX: r"https://www.securiteinfo.com/get/signatures/${customer_id}/",
        "!url_0hour": f"${{{PREFIX}}}securiteinfo0hour.hdb",
        "!url_old": f"${{{PREFIX}}}securiteinfoold.hdb",
        "!url_securiteinfo_mdb": f"${{{PREFIX}}}securiteinfo.mdb",
        "!url_securiteinfo_pdb": f"${{{PREFIX}}}securiteinfo.pdb",
        "!url_securiteinfo_yara": f"${{{PREFIX}}}securiteinfo.yara",
        "url_android": f"${{{PREFIX}}}securiteinfoandroid.hdb",
        "url_ascii": f"${{{PREFIX}}}securiteinfoascii.hdb",
        "url_html": f"${{{PREFIX}}}securiteinfohtml.hdb",
        "url_javascript": f"${{{PREFIX}}}javascript.ndb",
        "url_pdf": f"${{{PREFIX}}}securiteinfopdf.hdb",
        "url_securiteinfo": f"${{{PREFIX}}}securiteinfo.hdb",
        "url_securiteinfo_ign2": f"${{{PREFIX}}}securiteinfo.ign2",
        "url_spam_marketing": f"${{{PREFIX}}}spam_marketing.ndb",
    }
}
