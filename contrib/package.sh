#!/usr/bin/env bash
# vim: ts=4 sw=4 noet
#
# Script to package fangfrisch for distribution and to handle PyPI uploads.
# You need Python modules 'wheel' and 'twine' to publish to PyPI, and
# Ruby Gems 'asciidoctor' and 'asciidoctor-pdf' to generate HTML/PDF
# documentation.

set -euo pipefail

usage() {
	local bn
	bn=$(basename "$0")
	cat >&2 <<EOT
Usage: ${bn} {clean | dist | pypi}
       ${bn} setver {version}
EOT
	exit 1
}

clean() {
	rm -fr build/* dist/* src/*egg-info
}

dist() {
	python -m build
}

pypi() {
	twine upload dist/*
}

setver() {
	[[ $# -gt 0 ]] || usage
	local v=$1 s=(/usr/bin/sed -i '' -E)
	"${s[@]}" "s/^(version).+/\\1 = \"$v\"/" pyproject.toml
	"${s[@]}" "s/^(__version__).+/\\1 = \"$v\"/" src/fangfrisch/__init__.py
	"${s[@]}" "s/^(:revnumber:).+/\\1 $v/" docs/fangfrisch.adoc
}

main() {
	[[ $# -gt 0 ]] || usage
	local arg=$1
	shift
	case "${arg}" in
	clean)
		rm -fr build/* dist/* src/*egg-info
		;;
	dist | setver | pypi)
		# shellcheck disable=1091
		. .venv/bin/activate
		"${arg}" "$@"
		;;
	*)
		usage
		;;
	esac
}

main "$@"
