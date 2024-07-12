#!/usr/bin/env -S bash

server=$(ps -aef | grep -v grep | grep -E -o 'uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty' | sort -u)

echo $server
echo ---
echo ''
echo '```'
wrk http://127.0.0.1:8000 -d 10 -t 2 -c 200
echo '```'
