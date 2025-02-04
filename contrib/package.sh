#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Script to package fangfrisch for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-pdf' to generate HTML/PDF
# documentation.

set -euo pipefail

function usage() {
	local bn
	bn=$(basename "$0")
	echo "Usage: ${bn} {clean | dist | pypi}" >&2
	echo "       ${bn} setver {version}" >&2
	exit 1
}

function do_clean() {
	rm -fr build/* dist/* src/*egg-info
}

function do_dist() {
	# python -m build --no-isolation --skip-dependency-check
	python -m build
}

function do_pypi() {
	twine upload dist/*
}

function do_setver() {
	[ $# -gt 0 ] || usage
	local s=(/usr/bin/sed -i '' -E)
	"${s[@]}" "s/^version.+/version = \"${1}\"/" pyproject.toml
	"${s[@]}" "s/^__version.+/__version__ = '${1}'/" src/fangfrisch/__init__.py
	"${s[@]}" "s/^v[^ ]+ {docdate}$/v${1}, {docdate}/" docs/fangfrisch.adoc
}

[ $# -gt 0 ] || usage
arg="${1}"
shift
case "${arg}" in
clean)
	do_"${arg}"
	;;
dist | setver | pypi)
	# shellcheck disable=1091
	. .venv/bin/activate
	do_"${arg}" "$@"
	;;
*)
	usage
	;;
esac
unset arg
