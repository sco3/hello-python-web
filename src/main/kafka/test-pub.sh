#!/usr/bin/env -S bash

set -xueo pipefail

SIZE=${1:-1048664}

# limit total size to ~ 8g
TOTAL=8000000000
NUM=$(($TOTAL/$SIZE))


~/prg/kafka/bin/kafka-producer-perf-test.sh \
--producer-props bootstrap.servers=localhost:33001 max.request.size=1100000 \
--topic asdf   \
--throughput  -1  \
--num-records $NUM \
--record-size $SIZE | tee $0.out.$SIZE

