import argparse
import sys

from fangfrisch.config import config

parser = argparse.ArgumentParser()
parser.add_argument('action', help='Action to perform')
parser.add_argument('--conf', default=None, help='Configuration file (no default)')
args = parser.parse_args()
if not config.init(args.conf):
    print(f'Cannot parse configuration file: {args.conf}', file=sys.stderr)
    sys.exit(1)
if 'dumpconf' == args.action:
    config.dump()
else:
    print(f'Unknown action: {args.action}', file=sys.stderr)
    sys.exit(1)
