#!/usr/bin/env -S bash

set -xueo pipefail
source ./00-sizes.sh


host=$(rpk cluster info -b | tail -n 1 | awk '{print $2}')





~/prg/kafka/bin/kafka-producer-perf-test.sh \
--producer-props bootstrap.servers=$host:9092 max.request.size=1100000 \
--topic asdf   \
--throughput  -1  \
--num-records $NUM \
--record-size $SIZE | tee $OUT


grep "sent" $OUT | awk '{print $3 " " $4 }' > $OUT.msgs
#| awk '{ print $4 " " $5' > $OUT.msgs

