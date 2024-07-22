#!/usr/bin/env -S bash

server=$(ps -aef | grep -v grep | \
grep -E -o 'uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty|JerseyGrizzly|Vertx' \
| sort -u)

data=$(cat poetry.lock | tr ' ' '_')


echo $server
echo ---
echo ''
echo '```'
wrk http://127.0.0.1:8000/long -d 10 -t 1 -c 1 -s post.lua
echo '```'
