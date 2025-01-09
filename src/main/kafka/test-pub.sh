#!/usr/bin/env -S bash

set -xueo pipefail
source ./00-sizes.sh


rm -rf $OUT $OUT.msgs


~/prg/kafka/bin/kafka-producer-perf-test.sh \
--producer-props bootstrap.servers=localhost:33001 max.request.size=1100000 \
--topic asdf   \
--throughput  -1  \
--num-records $NUM \
--record-size $SIZE | tee $OUT


grep "sent" $OUT | awk '{print $4 " " $5 }' | tail -n 1 > $OUT.msgs

