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

import unittest
from typing import List

from fangfrisch.task import Task
from fangfrisch.task import add_task
from tests import FangfrischTest


class TaskTests(FangfrischTest):
    FIRST_COMMAND = "/invalid/command/path"

    def setUp(self) -> None:
        super().setUpClass()
        self.tasks: List[Task] = list()
        self.tasks.append(Task(command=self.FIRST_COMMAND, timeout=1))

    def test_add_task1(self):
        t = add_task(self.tasks, "c2", timeout=2)
        self.assertTrue(isinstance(t, Task))

    def test_add_task2(self):
        t = add_task(tasks=self.tasks, command=self.FIRST_COMMAND, timeout=3)
        self.assertIsNone(t)

    def test_complete1(self):
        for t in self.tasks:
            self.assertNotEqual(0, t.complete())

    def test_complete2(self):
        t = add_task(self.tasks, "echo", timeout=3)
        self.assertEqual(0, t.complete())


if __name__ == "__main__":
    unittest.main()
