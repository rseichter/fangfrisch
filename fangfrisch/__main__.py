import argparse
import sys

from fangfrisch.config import config
from fangfrisch.logging import log
from fangfrisch.refresh import refresh_all

parser = argparse.ArgumentParser()
parser.add_argument('action', help='Action to perform')
parser.add_argument('-c', '--conf', default=None, help='Configuration file (no default)')
args = parser.parse_args()
if not config.init(args.conf):
    log.error(f'Cannot parse configuration file: {args.conf}')
    sys.exit(1)
if 'dumpconf' == args.action:
    config.dump()
elif 'refresh' == args.action:
    refresh_all()
else:
    log.error(f'Unknown action: {args.action}')
    sys.exit(1)
