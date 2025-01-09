#!/usr/bin/env -S bash

set -xueo pipefail
./01-reset.sh
source 00-sizes.sh

nats bench test --no-progress --js --purge --pub 1 --sub 1 --size $SIZE --msgs $NUM --maxbytes $MAX  --csv $0.$SIZE.csv 2>&1 | tee $0.out.$SIZE
