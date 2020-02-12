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
along with Foobar. If not, see <https://www.gnu.org/licenses/>.
"""
import os
from typing import List

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


class ClamavRefresh:
    def __init__(self, args) -> None:
        self.args = args

    @staticmethod
    def collect_clamav_items() -> List[ClamavItem]:
        clamav_items = []
        for section in config.sections():
            if not config.is_enabled(section):
                continue
            base_url = config.base_url(section)
            if base_url:
                for option in config.options(section):
                    if option.startswith('url_'):
                        value = config.get(section, option)
                        item = ClamavItem(section, option, base_url + value, config.integrity_check(section),
                                          os.path.join(config.local_dir(section), value),
                                          config.max_age(section))
                        clamav_items.append(item)
        return clamav_items

    def refresh(self, ci: ClamavItem) -> bool:
        try:
            if self.args.force:
                log.debug(f'{ci.url} refresh forced')
            elif not RefreshLog.refresh_required(ci.url, ci.max_age):
                log.debug(f'{ci.url} skipped (no refresh required)')
                return False
            r = requests.get(ci.url)
            if r.status_code != requests.codes.ok:
                log.error(f'Failed to download data file: {r.status_code} {r.reason}')
                return False
            if ci.check:
                url = f'{ci.url}.{ci.check}'
                r_checksum = requests.get(url)
                if r_checksum.status_code != requests.codes.ok:
                    log.error(f'Failed to download checksum file: {r_checksum.status_code} {r_checksum.reason}')
                    return False
                digest = r_checksum.text.split(' ')[0]
                if not check_integrity(r.content, ci.check, digest):
                    log.error(f'Checksum mismatch (expected {digest})')
                    return False
            log.info(f'Updating {ci.path}')
            with open(ci.path, 'wb') as f:
                f.write(r.content)
                RefreshLog.stamp_by_url(ci.url)
        except OSError as e:  # pragma: no cover
            log.exception(e)
        return True

    def refresh_all(self) -> int:
        count = 0
        for clamav_item in self.collect_clamav_items():
            if self.refresh(clamav_item):
                count += 1
        return count
