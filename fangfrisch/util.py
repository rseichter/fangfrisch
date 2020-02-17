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
import hashlib
import re

_hr_bytes_pattern = re.compile(r'(\d+)([KM]B?)?', re.IGNORECASE)
_hr_time_pattern = re.compile(r'(\d+)([dhm])', re.IGNORECASE)
_hr_bytes_multipliers = {
    'K': 10 ** 3,
    'KB': 2 ** 10,
    'M': 10 ** 6,
    'MB': 2 ** 20,
}
_hr_time_multipliers = {
    'd': 24 * 60,
    'h': 60,
    'm': 1,
}


def check_integrity(content, algorithm: str, expected: str):
    if not algorithm:
        return True, None
    _hash = hashlib.new(algorithm)
    _hash.update(content)
    digest = _hash.hexdigest()
    if digest != expected:
        return False, f'{algorithm} digest mismatch (expected {expected}, got {digest})'
    return True, None


def parse_hr_bytes(s: str) -> int:
    match = _hr_bytes_pattern.fullmatch(s)
    if match:
        i = int(match[1])
        if match[2]:
            m = _hr_bytes_multipliers[match[2].upper()]
        else:
            m = 1
        return i * m
    return -1


def parse_hr_time(s: str) -> int:
    match = _hr_time_pattern.fullmatch(s)
    if match:
        i = int(match[1])
        m = _hr_time_multipliers[match[2].lower()]
        return i * m
    return -1
