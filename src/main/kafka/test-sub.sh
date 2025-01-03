#!/usr/bin/env -S bash

set -xueo pipefail

SIZE=${1:-1048664}

# limit total size to ~ 7g
TOTAL=8000000000
NUM=$(($TOTAL/$SIZE))
OUT=$0.out.$SIZE


~/prg/kafka/bin/kafka-consumer-perf-test.sh \
--bootstrap-server localhost:33001  \
--topic asdf --messages $NUM  | tee $OUT


awk -F',' '{ print $6}' $OUT > $OUT.msg.per.sec

