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
import os
from subprocess import CalledProcessError
from subprocess import CompletedProcess
from subprocess import run
from typing import List
from urllib.parse import urlparse

import requests

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.logging import log
from fangfrisch.util import check_integrity


class ClamavItem:
    def __init__(self, section, option, url, check, path, max_age) -> None:
        self.check = check
        self.max_age = max_age
        self.option = option
        self.path = path
        self.section = section
        self.url = url


def _clamav_items() -> List[ClamavItem]:
    item_list = []
    for section in config.sections():
        if not config.is_enabled(section):
            continue
        for option in config.options(section):
            check = config.integrity_check(section)
            max_age = config.max_age(section)
            if option.startswith('url_'):
                url = config.get(section, option)
                path: str = urlparse(url).path
                slash_pos = path.rfind('/')  # returns -1 if not found
                path = os.path.join(config.local_dir(section), path[slash_pos + 1:])
                item = ClamavItem(section, option, url, check, path, max_age)
                item_list.append(item)
    return item_list


def _get_digest(ci: ClamavItem):
    if not ci.check:
        return True, None
    r = requests.get(f'{ci.url}.{ci.check}')
    if r.status_code != requests.codes.ok:
        log.error(f'Failed to download checksum file: {r.status_code} {r.reason}')
        return False, None
    digest = r.text.split(' ')[0]
    return True, digest


def _get_payload(ci: ClamavItem):
    r = requests.get(ci.url)
    if r.status_code != requests.codes.ok:
        log.error(f'Failed to download data file: {r.status_code} {r.reason}')
        return False, None
    return True, r.content


class ClamavRefresh:
    def __init__(self, args) -> None:
        self.args = args

    def refresh(self, ci: ClamavItem) -> bool:
        """Refresh a single ClamAV item.

        :param ci: Item to refresh.
        :return: True if new payload data was written, False otherwise.
        """
        try:
            if self.args.force:
                log.debug(f'{ci.url} refresh forced')
            elif not RefreshLog.is_outdated(ci.url, ci.max_age):
                log.debug(f'{ci.url} below max age')
                return False
            status, digest = _get_digest(ci)
            if not status:
                return False
            if RefreshLog.digest_matches(ci.url, digest):
                log.debug(f'{ci.url} unchanged')
                RefreshLog.update(ci.url, digest)  # Update timestamp
                return False
            status, payload = _get_payload(ci)
            if not status:
                return False
            if not check_integrity(payload, ci.check, digest):
                log.error(f'{ci.url} integrity check failed')
                return False
            log.info(f'Updating {ci.path}')
            with open(ci.path, 'wb') as f:
                f.write(payload)
                RefreshLog.update(ci.url, digest)  # Update digest and timestamp
        except OSError as e:  # pragma: no cover
            log.exception(e)
        return True

    def refresh_all(self) -> int:
        count = 0
        for clamav_item in _clamav_items():
            if self.refresh(clamav_item):
                count += 1
        _exec = config.on_update_exec()
        if count > 0 and _exec:
            try:
                timeout = int(config.on_update_timeout())
                p: CompletedProcess = run(_exec, capture_output=True, encoding='utf-8', shell=True, timeout=timeout)
                if p.stdout:
                    log.info(p.stdout)
                if p.stderr:
                    log.error(p.stderr)
            except CalledProcessError as e:  # pragma: no cover
                log.exception(e)
        return count
