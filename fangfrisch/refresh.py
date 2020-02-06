import os
from collections import namedtuple
from typing import List

import requests

from fangfrisch.config import config
from fangfrisch.logging import log
from fangfrisch.util import check_sha256
from fangfrisch.util import write_binary

UrlTuple = namedtuple('UrlTuple', 'section option url check path')


def collect_url_tuples() -> List[UrlTuple]:
    tuples = []
    for section in config.sections():
        base_url = config.base_url(section)
        if base_url:
            for option in config.options(section):
                if option.startswith('url_'):
                    value = config.get(section, option)
                    url = base_url + value
                    tuples.append(UrlTuple(section, option, url, config.integrity_check(section),
                                           os.path.join(config.local_dir(section), value)))
    return tuples


def refresh_all() -> int:
    count = 0
    for ut in collect_url_tuples():
        if refresh(ut):
            count += 1
    return count


def refresh(ut: UrlTuple) -> bool:
    try:
        r = requests.get(ut.url)
        if r.status_code != requests.codes.ok:
            log.error(f'Failed to download data file: {r.status_code} {r.reason}')
            return False
        if 'sha256' == ut.check:
            r_checksum = requests.get(f'{ut.url}.{ut.check}')
            if r_checksum.status_code != requests.codes.ok:
                log.error(f'Failed to download checksum file: {r_checksum.status_code} {r_checksum.reason}')
                return False
            digest = r_checksum.text.split(' ')[0]
            if not check_sha256(r.content, digest):
                log.error(f'Checksum mismatch (expected {digest})')
                return False
        elif ut.check:
            log.error(f'Unsupported integrity check: {ut.check}')
            return False
        write_binary(r.content, ut.path)
    except OSError as e:  # pragma: no cover
        log.exception(e)
    return True
