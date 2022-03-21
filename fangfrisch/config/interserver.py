"""
Copyright © 2020-2022 Ralph Seichter
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
from fangfrisch.config import INTEGRITY_CHECK

interserver = {
    'interserver': {
        INTERVAL: '1h',
        MAX_SIZE: '100MB',
        PREFIX: r'http://sigs.interserver.net/',
        INTEGRITY_CHECK: 'disabled'
        'url_interserver256': f'${{{PREFIX}}}interserver256.hdb',
        'url_interservertopline': f'${{{PREFIX}}}interservertopline.db',
        'url_shell': f'${{{PREFIX}}}shell.ldb',
        'url_whitelist': f'${{{PREFIX}}}whitelist.fp',
    }
}
