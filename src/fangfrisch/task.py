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

from typing import List
from typing import Optional

from fangfrisch.log import log_debug
from fangfrisch.log import log_error
from fangfrisch.log import log_exception
from fangfrisch.log import log_info
from fangfrisch.util import run_command


class Task:
    def __init__(self, command: str, timeout: int) -> None:
        self.command = command
        self.timeout = timeout

    def __str__(self):  # pragma: no cover
        return f"Task(command={{{self.command}}}, timeout={self.timeout})"

    def complete(self) -> int:
        rc = run_command(
            command=self.command,
            timeout=self.timeout,
            callback_stdout=log_info,
            callback_stderr=log_error,
            callback_exception=log_exception,
        )
        log_debug(f"{self} returned code {rc}")
        return rc


def add_task(tasks: List[Task], command: str, timeout: int) -> Optional[Task]:
    for task in tasks:
        if task.command == command:
            log_debug(f"Ignoring duplicate: {command}")
            return None
    task = Task(command=command, timeout=timeout)
    tasks.append(task)
    log_debug(f"{task} added")
    return task
