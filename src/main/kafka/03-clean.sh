

source 00-dir.sh

set -xueo pipefail

./02-stop.sh || echo ok
sleep 2
rm -rf $DATADIR/*
rm logs/*
