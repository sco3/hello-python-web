#!/usr/bin/env -S bash

set -xueo pipefail
source ./00-sizes.sh

rm -rf $OUT $OUT.msgs

~/prg/kafka/bin/kafka-consumer-perf-test.sh \
 --bootstrap-server localhost:$PORT  \
 --topic asdf --messages $NUM  2>&1| tee $OUT

awk -F',' '($6!=""){ print $6}' $OUT | grep -v epoch > $OUT.msgs

