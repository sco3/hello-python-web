#!/usr/bin/env -S bash

name=consumer_limits

for i in 1 2  ; do
   nats consumer sub stream_retention_limits "${name}1"  > .$i.out 2>&1 &
done
