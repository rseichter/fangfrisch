#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Script to package fangfrisch for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-pdf' to generate HTML/PDF
# documentation.

set -euo pipefail

function usage() {
	local bn
	bn="$(basename $0)"
	echo "Usage: ${bn} {clean | dist}" >&2
	echo "       ${bn} upload [repository]" >&2
	echo "       ${bn} setver {version}" >&2
	exit 1
}

function do_clean() {
	/bin/rm -r build/* dist/* || true
}

function do_dist() {
	python setup.py sdist bdist_wheel
}

function do_upload() {
	twine upload dist/*
}

function do_setver() {
	[ $# -gt 0 ] || usage
	local sed="/usr/bin/sed -E"
	set -x
	${sed} -i "" -e "s/^v[^ ]+ {docdate}$/v${1}, {docdate}/" docs/fangfrisch.adoc
	${sed} -i "" -e "s/^__version.+/__version__ = '${1}'/" fangfrisch/__init__.py
	set +x
}

[ $# -gt 0 ] || usage
arg="$1"
shift
case "$arg" in
	clean)
		do_${arg}
		;;
	dist | setver | upload)
		source .venv/bin/activate
		do_${arg} "$@"
		;;
	*)
		usage
		;;
esac
