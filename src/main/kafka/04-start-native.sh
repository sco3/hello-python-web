#!/usr/bin/env -S bash

set -xueo pipefail

source 00-dir.sh

rm -rf target

tmux new -d -s kafka \
    ./kafka-server-999-SNAPSHOT-runner
