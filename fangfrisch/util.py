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


class StatusDataPair:
    def __init__(self, ok: bool, data=None) -> None:
        self.data = data
        self.ok = ok


def check_integrity(content, algorithm: str, expected: str) -> StatusDataPair:
    """Check integrity of a content object.

    :param content: Object to verify.
    :param algorithm: Mechanism used to calculate a digest.
    :param expected: Expected digest.
    :return: True if digests match, False otherwise.
    """
    if algorithm:
        _hash = hashlib.new(algorithm)
        _hash.update(content)
        digest = _hash.hexdigest()
        if digest != expected:
            message = f'{algorithm} digest mismatch (expected {expected}, got {digest})'
            return StatusDataPair(False, message)
    return StatusDataPair(True)


def parse_hr_bytes(s: str) -> int:
    """Parse human-readable bytes representation (e.g. 5MB, 250K)

    :param s: String to parse.
    :return: Number of bytes.
    """
    match = re.fullmatch(r'(\d+)([KM]B?)?', s, re.IGNORECASE)
    if match:
        _bytes = int(match[1])
        if match[2]:
            multipliers = {
                'K': 10 ** 3,
                'KB': 2 ** 10,
                'M': 10 ** 6,
                'MB': 2 ** 20,
            }
            m = multipliers[match[2].upper()]
        else:
            m = 1
        return _bytes * m
    return -1


def parse_hr_time(s: str) -> int:
    """Parse human-readable time representation (e.g. 2d, 3h, 20m)

    :param s: String to parse.
    :return: Number of minutes.
    """
    match = re.fullmatch(r'(\d+)([dhm])', s, re.IGNORECASE)
    if match:
        multipliers = {
            'd': 24 * 60,
            'h': 60,
            'm': 1,
        }
        minutes = int(match[1])
        m = multipliers[match[2].lower()]
        return minutes * m
    return -1
