#!/usr/bin/env bash
# vim:ts=4:noet
#
# Runs unittests for automx2. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data. This will also
# generate a HTML-based coverage report.

set -euo pipefail
source .venv/bin/activate

DIR='/tmp/fangfrisch/unittest'
DB="$DIR/db.sqlite"
if [ -d $DIR ]; then
	rm -r $DIR
fi
mkdir -p $DIR
sqlite3 $DB < tests/tests.sql

CONF='tests/tests.conf'
sed -i '' -e "s,^db_url.*,db_url = sqlite:///${DB}," $CONF

function usage() {
	echo "Usage: $(basename $0) [coverage]" >&2
	exit 1
}

function run_tests() {
	local cmd="$1"
	shift
	PYTHONPATH=. ${cmd} -m unittest discover tests/ -v "$@"
}

function run_coverage() {
	run_tests 'coverage run --source fangfrisch --omit fangfrisch/__main__.py'
	coverage html --rcfile=tests/coverage.rc
}

if [ $# -gt 0 ]; then
	if [ "$1" = "coverage" ]; then
		run_coverage
	else
		usage
	fi
else
	run_tests python
fi
