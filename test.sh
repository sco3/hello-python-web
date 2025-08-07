#!/usr/bin/env -S bash



./cpu-governor.sh
server=$(ps -aef | grep -v grep | \
grep -E -o 'node|uvicorn|fastwsgi|rust-minihttp|JavaJooby|JerseyNetty|JerseyJetty|JerseyGrizzly|Vertx|spring|main-v|fasthttp-go|go' \
| sort -u)

echo $server
echo ---
echo ''
echo '```'
wrk http://127.0.0.1:8000 -d 10 -t 2 -c 200
#-H "Hello, world\n"
echo '```'
