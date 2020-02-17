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
along with Fangfrisch. If not, see <https://www.gnu.org/licenses/>.
"""
import requests
from requests import Response

from fangfrisch import __version__
from fangfrisch.logging import log

CONTENT_LENGTH = 'Content-Length'

_session = requests.Session()
_session.headers['User-Agent'] = f'fangfrisch/{__version__}'


class ClamavItem:
    def __init__(self, section, option, url, check, path, max_age, max_size) -> None:
        self.check = check
        self.max_age = max_age
        self.max_size = max_size
        self.option = option
        self.path = path
        self.section = section
        self.url = url


def _content_length(r: Response, limit: int):
    if CONTENT_LENGTH not in r.headers:  # pragma: no cover
        log.error(f'Response is missing {CONTENT_LENGTH} header')
        return -1, False
    length = int(r.headers[CONTENT_LENGTH])
    if length > limit:
        log.error(f'{r.url} size exceeds defined limit ({length}/{limit})')
        return length, False
    return length, True


def _get_data(url, max_size: int):
    r = _session.get(url)
    if r.status_code != requests.codes.ok:
        log.error(f'{url} download failed: {r.status_code} {r.reason}')
        return False, None
    length, permitted = _content_length(r, max_size)
    if not permitted:
        return False, None
    return True, r


def get_digest(ci: ClamavItem, max_size: int = 1024):
    if not ci.check:
        return True, None
    status, r = _get_data(f'{ci.url}.{ci.check}', max_size)
    if not status:
        return False, None
    digest = r.text.split(' ')[0]  # Returns original text if no space is found
    return True, digest


def get_payload(ci: ClamavItem):
    status, r = _get_data(ci.url, ci.max_size)
    if not status:
        return False, None
    return True, r.content
