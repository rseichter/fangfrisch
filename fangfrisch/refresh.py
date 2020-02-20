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
from typing import List
from urllib.parse import urlparse

from fangfrisch import ClamavItem
from fangfrisch.config.config import config
from fangfrisch.db import RefreshLog
from fangfrisch.download import get_digest
from fangfrisch.download import get_payload
from fangfrisch.logging import log
from fangfrisch.util import check_integrity
from fangfrisch.util import run_command


def _clamav_items() -> List[ClamavItem]:
    item_list = []
    for section in config.sections():
        if not config.is_enabled(section):
            continue
        for option in config.options(section):
            max_size = config.max_size(section)
            if max_size < 1:
                log.error(f"Cannot parse max size for section '{section}'")
                continue
            local_dir = config.local_dir(section)
            if local_dir:
                os.makedirs(local_dir, exist_ok=True)
            if option.startswith('url_'):
                url = config.get(section, option)
                stem = option[4:]
                filename = config.get(section, f'filename_{stem}')
                if not filename:
                    url_path: str = urlparse(url).path
                    slash_pos = url_path.rfind('/')  # returns -1 if not found
                    filename = url_path[slash_pos + 1:]
                if local_dir:
                    filename = os.path.join(local_dir, filename)
                item_list.append(ClamavItem(
                    section=section,
                    option=option,
                    url=url,
                    check=config.integrity_check(section),
                    path=filename,
                    interval=config.interval(section),
                    max_size=max_size,
                    on_update=config.get(section, f'on_update_{stem}')
                ))
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
            if digest.data and RefreshLog.digest_matches(ci.url, digest.data):
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
            with open(ci.path, 'wb') as f:
                size = f.write(payload.data)
                log.info(f'{ci.path} updated ({size} bytes)')
                RefreshLog.update(ci.url, digest.data)  # Update digest and timestamp
        except OSError as e:  # pragma: no cover
            log.exception(e)
        return True

    def refresh_all(self) -> int:
        count = 0
        for ci in _clamav_items():
            if self.refresh(ci):
                command = ci.on_update
                if command:
                    run_command(command, config.on_update_timeout(), log, path=ci.path)
                count += 1
        command = config.on_update_exec()
        if count > 0 and command:
            run_command(command, config.on_update_timeout(), log)
        return count
