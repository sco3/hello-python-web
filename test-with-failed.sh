#!/usr/bin/env -S bash

server=$(ps -aef | grep -v grep | \
grep -E -o 'uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty|JerseyGrizzly|Vertx|spring|main-v|fasthttp-go|go' \
| sort -u)

echo $server
echo ---
echo ''
echo '```'
wrk http://127.0.0.1:8000 -d 10 -t 2000 -c 2000 -s test-with-failed.lua
#-H "Hello, world\n"
echo '```'
