#!/usr/bin/env -S bash

set -ueo pipefail


function in-poetry-run {
   #stubgen test -o ~/tmp/stubs
   cd src/main/python
   mypyc -p nats
}

if [ "${1:-''}" == "poetry" ]; then
   in-poetry-run
else
   poetry run $(readlink -f "$0") poetry
fi


