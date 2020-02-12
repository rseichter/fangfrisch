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
import argparse
import sys

from fangfrisch.config.config import config
from fangfrisch.logging import log
from fangfrisch.refresh import ClamavRefresh

parser = argparse.ArgumentParser()
parser.add_argument('action', help='Action to perform')
parser.add_argument('-c', '--conf', default=None, help='Configuration file')
parser.add_argument('-f', '--force', default=False, action='store_true', help='Force action (default: False)')
args = parser.parse_args()
if not config.init(args.conf):
    log.error(f'Cannot parse configuration file: {args.conf}')
    sys.exit(1)
if 'dumpconf' == args.action:
    config.dump()
elif 'refresh' == args.action:
    ClamavRefresh(args).refresh_all()
else:
    log.error(f'Unknown action: {args.action}')
    sys.exit(1)
