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
    ClamavRefresh().refresh_all(args.force)
else:
    log.error(f'Unknown action: {args.action}')
    sys.exit(1)
