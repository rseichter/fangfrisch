#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Runs unittests for Fangfrisch. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data. This will also
# generate a HTML-based coverage report.

set -euo pipefail
# shellcheck disable=1091
. .venv/bin/activate

declare -r DIR=/tmp/fangfrisch/unittest
declare -r DB="$DIR"/db.sqlite
rm -fr $DIR
mkdir -p $DIR
sqlite3 $DB <tests/tests.sql
sed -i "" "s,^db_url.*,db_url = sqlite:///${DB}," tests/tests.conf

usage() {
	echo "Usage: $(basename "$0") [coverage]" >&2
	exit 1
}

unittest() {
	PYTHONPATH=.:src "$@" -m unittest discover tests/ -v
}

if [[ $# -eq 0 ]]; then
	unittest python
elif [[ $1 == coverage ]]; then
	unittest coverage run --source fangfrisch --omit fangfrisch/__main__.py
	coverage html --rcfile=tests/coverage.rc
else
	usage
fi
