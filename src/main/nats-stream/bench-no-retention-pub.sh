#!/usr/bin/env -S bash

set -xueo pipefail

SIZE=${1:-1048664}

# limit total size to ~ 8g
TOTAL=8000000000
NUM=$(($TOTAL/$SIZE/2))


nats bench test --no-progress --js --pub 1  --size $SIZE --msgs $NUM --maxbytes 8G   2>&1 | tee $0.out.$SIZE
