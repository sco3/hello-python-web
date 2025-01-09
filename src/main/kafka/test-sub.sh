#!/usr/bin/env -S bash

set -xueo pipefail
source ./00-sizes.sh


~/prg/kafka/bin/kafka-consumer-perf-test.sh \
 --bootstrap-server localhost:33001  \
 --topic asdf --messages $NUM  | tee $OUT

awk -F',' '($6!=""){ print $6}' $OUT | grep -v epoch > $OUT.msgs

