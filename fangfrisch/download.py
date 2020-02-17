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
from fangfrisch.util import StatusDataPair

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


def _content_length(r: Response, limit: int) -> StatusDataPair:
    if CONTENT_LENGTH not in r.headers:  # pragma: no cover
        log.error(f'Response is missing {CONTENT_LENGTH} header')
        return StatusDataPair(False, -1)
    length = int(r.headers[CONTENT_LENGTH])
    if length > limit:
        log.error(f'{r.url} size exceeds defined limit ({length}/{limit})')
        return StatusDataPair(False, length)
    return StatusDataPair(True, length)


def _download(url, max_size: int) -> StatusDataPair:
    r = _session.get(url)
    if r.status_code != requests.codes.ok:
        log.error(f'{url} download failed: {r.status_code} {r.reason}')
        return StatusDataPair(False)
    cl = _content_length(r, max_size)
    if not cl.ok:
        return StatusDataPair(False)
    return StatusDataPair(True, r)


def get_digest(ci: ClamavItem, max_size: int = 1024) -> StatusDataPair:
    if not ci.check:
        return StatusDataPair(True)
    d = _download(f'{ci.url}.{ci.check}', max_size)
    if not d.ok:
        return StatusDataPair(False)
    d = d.data.text.split(' ')[0]  # Returns original text if no space is found
    return StatusDataPair(True, d)


def get_payload(ci: ClamavItem) -> StatusDataPair:
    d = _download(ci.url, ci.max_size)
    if not d.ok:
        return StatusDataPair(False)
    return StatusDataPair(True, d.data.content)
