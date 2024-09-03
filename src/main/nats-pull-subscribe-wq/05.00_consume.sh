#!/usr/bin/env -S bash

name=consumer_work

for i in 1 2  ; do
   nats consumer sub stream_retention_work "${name}${i}"  > .$i.out 2>&1 &
done
