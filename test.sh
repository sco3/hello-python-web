#!/usr/bin/env -S bash

#set -ueo pipefail

function run_curl() {
	#> ${server}.$1.txt
	local i
	for ((i = 0; i < $2; i++)); do
		curl -s localhost:8000 >/dev/null
		#>>${server}.$1.txt
	done
}

function check() {
	ps -aef | grep $(basename $0) | grep -v grep | wc -l
}

function main() {
	echo $1 processes $2 requests
	for ((i = 0; i < $1; i++)); do
		run_curl $i $2 &
	done

	cnt=$(check)
	while ((cnt > 2)); do
		cnt=$(check)
		sleep 1
	done
}

server=$(ps -aef | grep -v grep | grep -E -o 'uvicorn|fastwsgi' | sort -u)

echo $server
time main 16 1000

#wc -l *.txt
