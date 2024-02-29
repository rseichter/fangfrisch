#!/usr/bin/env bash
# vim: ts=4 sw=4 noet ft=sh
#
# Example script to process Fangfrisch News.
#
# The caller is required to pass 1..n directories
# to be scanned for news items.

set -euo pipefail

declare -r MAILFROM="noreply@example.net"
declare -r MAILTO="alice@example.org"
declare -r SUBJECT="I have news for you"

die() {
	echo >&2 "$@"
	exit 1
}

usage() {
	die "Usage: $(basename "$0") {directory} [[directory] ...]"
}

print_header() {
	# Mail header must end with an empty line
	cat <<EOT
From: Fangfrisch News <$MAILFROM>
To: $MAILTO
Subject: $SUBJECT

EOT
}

report_news() {
	[ $# -ge 1 ] || usage
	local body counter dir fn
	body=$(mktemp)
	# shellcheck disable=SC2064
	trap "rm $body" EXIT
	counter=0
	for dir in "$@"; do
		[ -d "$dir" ] || die "$dir is not a directory"
		while IFS= read -r -d '' fn; do
			(( counter+=1 ))
			echo -e "\n### $fn:\n" >>"$body"
			cat "$fn" >>"$body"
		done < <(find "$dir" -type f -name "fangfrisch*.txt" -print0)
	done
	if [ $counter -gt 0 ]; then
		print_header
		cat "$body"
	fi
}

# When running in a terminal session, simply print
# the news. Otherwise, report the news via email.
if tty -s; then
	report_news "$@"
else
	report_news "$@" 2>&1 | /usr/sbin/sendmail -t
fi
