"""
Copyright © 2020-2025 Ralph Seichter

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
import os
import re
from string import Formatter
from subprocess import CompletedProcess
from subprocess import run
from typing import Optional

_byte_multipliers = {"K": 10**3, "KB": 2**10, "M": 10**6, "MB": 2**20}
_byte_pattern = re.compile(r"(\d+)([KM]B?)?", re.IGNORECASE)
_minute_multipliers = {"d": 24 * 60, "h": 60, "m": 1}
_minute_pattern = re.compile(r"(\d+)([dhm])", re.IGNORECASE)


class StatusDataPair:
    def __init__(self, ok: bool, data=None) -> None:
        self.data = data
        self.ok = ok


def check_integrity(content, algorithm: str, expected: str) -> StatusDataPair:
    """Check integrity of a content object.

    :param content: Object to verify.
    :param algorithm: Mechanism used to calculate a digest.
    :param expected: Expected digest.
    :return: True/None if calculated and expected digests match, False/Message otherwise.
    """
    if algorithm:
        _hash = hashlib.new(algorithm)
        _hash.update(content)
        digest = _hash.hexdigest()
        if digest != expected:
            message = f"{algorithm} digest mismatch (expected {expected}, got {digest})"
            return StatusDataPair(False, message)
    return StatusDataPair(True)


def parse_hr_bytes(s: str) -> int:
    """Parse human-readable bytes representation (e.g. 5MB, 250K)

    :param s: String to parse.
    :return: Number of bytes or -1 for parsing errors.
    """
    m = _byte_pattern.fullmatch(s)
    if m:
        if m[2]:
            multiplier = _byte_multipliers[m[2].upper()]
        else:
            multiplier = 1
        return int(m[1]) * multiplier
    return -1


def parse_hr_time(s: str) -> int:
    """Parse human-readable time representation (e.g. 2d, 3h, 20m)

    :param s: String to parse.
    :return: Number of minutes or -1 for parsing errors.
    """
    m = _minute_pattern.fullmatch(s)
    if m:
        multiplier = _minute_multipliers[m[2].lower()]
        return int(m[1]) * multiplier
    return -1


def run_command(
    command: str, timeout: int, callback_stdout, callback_stderr, callback_exception, *args, **kwargs
) -> Optional[int]:
    """Execute a command in a subprocess.

    :param command: Command string.
    :param timeout: Command timeout in seconds.
    :param callback_stdout: Callback to process subcommand stdout.
    :param callback_stderr: Callback to process subcommand stderr.
    :param callback_exception: Call if the subcommand raises an exception.
    """
    # noinspection PyTypeChecker
    p: CompletedProcess = None
    try:
        command = Formatter().vformat(command, args, kwargs)
        p = run(command, capture_output=True, encoding="utf-8", shell=True, timeout=timeout)
        if p.stdout:
            callback_stdout(p.stdout)
        if p.stderr:
            callback_stderr(p.stderr)
    except Exception as e:
        callback_exception(e)
    if p is not None:
        return p.returncode


def remove_if_exists(path: str, log_callback) -> None:
    if path and os.path.exists(path):
        log_callback(f"Removing file {path}")
        os.remove(path)
