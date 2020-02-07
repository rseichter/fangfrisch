import os
from typing import List

import requests

from fangfrisch.config import config
from fangfrisch.logging import log
from fangfrisch.util import check_sha256


class ClamavItem:
    def __init__(self, section, option, url, check, path) -> None:
        self.check = check
        self.option = option
        self.path = path
        self.section = section
        self.url = url


class ClamavRefresh:
    @staticmethod
    def collect_clamav_items() -> List[ClamavItem]:
        result = []
        for section in config.sections():
            base_url = config.base_url(section)
            if base_url:
                for option in config.options(section):
                    if option.startswith('url_'):
                        value = config.get(section, option)
                        item = ClamavItem(section, option, base_url + value, config.integrity_check(section),
                                          os.path.join(config.local_dir(section), value))
                        result.append(item)
        return result

    @staticmethod
    def refresh(ci: ClamavItem) -> bool:
        try:
            r = requests.get(ci.url)
            if r.status_code != requests.codes.ok:
                log.error(f'Failed to download data file: {r.status_code} {r.reason}')
                return False
            if 'sha256' == ci.check:
                r_checksum = requests.get(f'{ci.url}.{ci.check}')
                if r_checksum.status_code != requests.codes.ok:
                    log.error(f'Failed to download checksum file: {r_checksum.status_code} {r_checksum.reason}')
                    return False
                digest = r_checksum.text.split(' ')[0]
                if not check_sha256(r.content, digest):
                    log.error(f'Checksum mismatch (expected {digest})')
                    return False
            elif ci.check:
                log.error(f'Unsupported integrity check: {ci.check}')
                return False
            with open(ci.path, 'wb') as f:
                f.write(r.content)
        except OSError as e:  # pragma: no cover
            log.exception(e)
        return True

    def refresh_all(self) -> int:
        count = 0
        for ci in self.collect_clamav_items():
            if self.refresh(ci):
                count += 1
        return count
