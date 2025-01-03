#!/usr/bin/env -S bash


source 00-sizes.sh

nats bench test --no-progress --js --pub 1  --size $SIZE --msgs 5 --maxbytes 8G   2>&1 | tee $0.out.$SIZE
