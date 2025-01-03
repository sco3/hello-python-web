#!/usr/bin/env -S bash

source 00-sizes.sh

nats bench test --no-progress --js --pub 1 --sub 1 --size $SIZE --msgs $NUM --maxbytes $MAX  --replicas 3 2>&1 | tee $0.out.$SIZE
