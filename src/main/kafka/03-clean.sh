source 00-dir.sh

set -xueo pipefail

./02-stop.sh || echo ok
sleep 2
rm -rf $DATADIR/*
pwd
rm $(dirname $(readlink -f $0))/logs/* || echo ok logs were not found 
