#!/usr/bin/env -S bash

src=src/main/python/square/nats

set -ueo pipefail

dir=$(dirname $(readlink -f "$0"))

function in-poetry-run {
	if [[ ! -d $dir/stubs ]]; then
		stubgen -p observable -o $dir/stubs
	fi
	cd $src
	MYPYPATH=$dir/stubs mypyc *.py
}

if [ "${1:-''}" == "poetry" ]; then
	in-poetry-run
else
	poetry run $(readlink -f "$0") poetry
fi
