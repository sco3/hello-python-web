#!/usr/bin/env -S bash

server=$(ps -aef | grep -v grep | \
grep -E -o 'uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty|JerseyGrizzly|Vertx|spring|main-v|fasthttp-go|go' \
| sort -u)

echo $server
echo ---
echo ''
echo '```'
wrk2  -R 60000 -s test-with-failed.lua  -t 500 -c 500 http://127.0.0.1:8000
#-H "Hello, world\n"
echo '```'
