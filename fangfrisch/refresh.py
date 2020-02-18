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

from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.download import ClamavItem
from fangfrisch.download import get_digest
from fangfrisch.download import get_payload
from fangfrisch.logging import log
from fangfrisch.util import check_integrity


def _clamav_items() -> List[ClamavItem]:
    item_list = []
    for section in config.sections():
        if not config.is_enabled(section):
            continue
        for option in config.options(section):
            local_dir = config.local_dir(section)
            max_size = config.max_size(section)
            if max_size < 1:
                log.error(f"Cannot parse max size for section '{section}'")
                continue
            os.makedirs(local_dir, exist_ok=True)
            if option.startswith('url_'):
                url = config.get(section, option)
                path: str = urlparse(url).path
                slash_pos = path.rfind('/')  # returns -1 if not found
                path = os.path.join(local_dir, path[slash_pos + 1:])
                item = ClamavItem(section, option, url, config.integrity_check(section),
                                  path, config.interval(section), max_size)
                item_list.append(item)
    return item_list


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
            elif not RefreshLog.is_outdated(ci.url, ci.interval):
                log.debug(f'{ci.url} below max age')
                return False
            digest = get_digest(ci)
            if not digest.ok:
                return False
            if RefreshLog.digest_matches(ci.url, digest.data):
                log.debug(f'{ci.url} unchanged')
                RefreshLog.update(ci.url, digest.data)  # Update timestamp
                return False
            payload = get_payload(ci)
            if not payload.ok:
                return False
            integrity = check_integrity(payload.data, ci.check, digest.data)
            if not integrity.ok:
                log.warning(f'{ci.url} {integrity.data}')
                return False
            log.info(f'Updating {ci.path}')
            with open(ci.path, 'wb') as f:
                f.write(payload.data)
                RefreshLog.update(ci.url, digest.data)  # Update digest and timestamp
        except OSError as e:  # pragma: no cover
            log.exception(e)
        return True

    def refresh_all(self) -> int:
        count = 0
        for ci in _clamav_items():
            if self.refresh(ci):
                count += 1
        _exec = config.on_update_exec()
        if count > 0 and _exec:
            try:
                timeout = config.on_update_timeout()
                p: CompletedProcess = run(_exec, capture_output=True, encoding='utf-8', shell=True, timeout=timeout)
                if p.stdout:
                    log.info(p.stdout)
                if p.stderr:
                    log.error(p.stderr)
            except CalledProcessError as e:  # pragma: no cover
                log.exception(e)
        return count
