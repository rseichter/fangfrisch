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

from fangfrisch.config import INTEGRITY_CHECK
from fangfrisch.config import INTERVAL
from fangfrisch.config import MAX_SIZE
from fangfrisch.config import PREFIX

interserver = {
    "interserver": {
        INTERVAL: "1h",
        INTEGRITY_CHECK: "disabled",
        MAX_SIZE: "5MB",
        PREFIX: r"http://sigs.interserver.net/",
        "!url_shell_hdb": f"${{{PREFIX}}}shell.hdb",
        "!url_shellb_db": f"${{{PREFIX}}}shellb.db",
        "url_interserver256": f"${{{PREFIX}}}interserver256.hdb",
        "url_shell_ldb": f"${{{PREFIX}}}shell.ldb",
        "filename_shell_ldb": "interservershell.ldb",
        "url_topline": f"${{{PREFIX}}}interservertopline.db",
        "url_whitelist_fp": f"${{{PREFIX}}}whitelist.fp",
        "filename_whitelist_fp": "interserverwhitelist.fp",
    }
}
