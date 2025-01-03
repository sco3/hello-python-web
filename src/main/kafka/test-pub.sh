#!/usr/bin/env -S bash

SIZE=${1:-1024}

~/prg/kafka/bin/kafka-producer-perf-test.sh --producer-props 'bootstrap.servers=localhost:33001'  --topic asdf   --throughput  -1  --num-records 10000000 --record-size $SIZE | tee $0.out.$SIZE

