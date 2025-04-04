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

__version__ = "1.9.2"


class ClamavItem:
    def __init__(
        self, section, option, url, check, path, interval, max_size, on_update, connection_timeout, stem
    ) -> None:
        self.check = check
        self.connection_timeout = connection_timeout
        self.interval = interval
        self.max_size = max_size
        self.on_update = on_update
        self.option = option
        self.path = path
        self.section = section
        self.stem = stem
        self.url = url
