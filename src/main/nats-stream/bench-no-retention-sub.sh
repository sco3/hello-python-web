#!/usr/bin/env -S bash

set -xueo pipefail

SIZE=${1:-1048664}

# limit total size to ~ 8g
TOTAL=8000000000
NUM=$((90*$TOTAL/$SIZE/100))

nats bench test --no-progress --js --sub 1 --size $SIZE --msgs 5 --maxbytes 8G  2>&1 | tee $0.out.$SIZE
