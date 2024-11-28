#!/usr/bin/env -S bash

set -xueo pipefail

function clean_build() {
    rm -rf test
    rm -rf build
    find . -name \*.so -delete

}

function check() {
    uv run black "$@"
    uv run isort "$@"
    #5MYPYPATH=../../stubs uv run mypyc --check-untyped-defs --strict "$@"
    uv run pyright "$@"
    uv run pyre check | grep vcr || echo pyre check all files
    uv run pylint "$@"
}

cd $(dirname $0)

clean_build

test_files=$(find . -name \*.py)

check $test_files

clean_build
