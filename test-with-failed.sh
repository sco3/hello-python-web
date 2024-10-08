#!/usr/bin/env -S bash

server=$(ps -aef | grep -v grep | \
grep -E -o 'uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty|JerseyGrizzly|Vertx|spring|main-v|fasthttp-go|go' \
| sort -u)

echo $server
echo ---
echo ''
echo '```'
wrk2 http://127.0.0.1:8000 -r 1000 -d 120 -t 400 -c 400 -s test-with-failed.lua
#-H "Hello, world\n"
echo '```'
