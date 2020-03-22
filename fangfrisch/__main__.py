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
import argparse
import sys

from fangfrisch.config.config import config
from fangfrisch.db import DbMeta
from fangfrisch.dump import DumpDbEntries
from fangfrisch.logging import log
from fangfrisch.refresh import ClamavRefresh


def main() -> int:
    dumpconf = 'dumpconf'
    dumpmappings = 'dumpmappings'
    initdb = 'initdb'
    parser = argparse.ArgumentParser(description='Update and verify unofficial ClamAV signatures.')
    parser.add_argument('action', choices=[dumpconf, dumpmappings, initdb, 'refresh'])
    parser.add_argument('-c', '--conf', default=None, help='configuration file')
    parser.add_argument('-f', '--force', default=False, action='store_true', help='force action (default: False)')
    parser.add_argument('-p', '--provider', default='.', help='provider name filter (regular expression)')
    args = parser.parse_args()
    if not config.init(args.conf):
        log.error(f'Cannot parse configuration file: {args.conf}')
        sys.exit(1)
    if dumpconf == args.action:
        config.write(sys.stdout)
    elif dumpmappings == args.action:
        DumpDbEntries(args).print_url_path_mappings(sys.stdout)
    elif initdb == args.action:
        DbMeta().create_metadata(args.force)
    else:
        DbMeta.assert_version_match()
        ClamavRefresh(args).refresh_all()
    return 0


if __name__ == '__main__':
    sys.exit(main())
