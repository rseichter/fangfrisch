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
from fangfrisch.config import LOCAL_DIR
from fangfrisch.config import MAX_SIZE
from fangfrisch.config import ON_UPDATE_EXEC
from fangfrisch.config import PREFIX

fangfrischnews = {
    "fangfrischnews": {
        INTERVAL: "12h",
        LOCAL_DIR: "/tmp",
        MAX_SIZE: "100KB",
        "script": "/path/to/fangfrisch-has-news.sh",
        ON_UPDATE_EXEC: f"[ ! -x ${{script}} ] || ${{script}} ${{{LOCAL_DIR}}}",
        PREFIX: r"https://www.seichter.de/fangfrisch/",
        "url_alerts": f"${{{PREFIX}}}fangfrisch_alerts.txt",
        "url_news": f"${{{PREFIX}}}fangfrisch_news.txt",
    }
}
