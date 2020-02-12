#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Runs unittests for automx2. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data. This will also
# generate a HTML-based coverage report.

CONF='tests/tests.conf'
SETTINGS='tests/settings.sh'

set -e

source venv/bin/activate
if [ -f ${SETTINGS} ]; then
	source ${SETTINGS}
fi

if [ ! -f ${CONF} ]; then
	echo "Missing config file ${CONF}" >&2
	exit 1
fi

if [ ! -d /tmp/fangfrisch.sh/unittest ]; then
	mkdir -p /tmp/fangfrisch.sh/unittest
fi

function usage() {
	echo "Usage: $(basename $0) [coverage]" >&2
	exit 1
}

function run_tests() {
	local cmd="$1"
	shift
	PYTHONPATH=".:${PYTHONPATH}" $cmd -m unittest discover tests/ "$@"
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
