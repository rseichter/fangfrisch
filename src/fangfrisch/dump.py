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

from fangfrisch.db import RefreshLog


class DumpDbEntries:
    def __init__(self, args) -> None:
        self.args = args

    def print_url_path_mappings(self, outfile) -> None:
        r: RefreshLog
        for r in RefreshLog.url_path_mappings(self.args.provider):
            print(f"{r.provider}\t{r.url}\t{r.path}", file=outfile)
