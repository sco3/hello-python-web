

source 00-dir.sh

set -xueo pipefail

function del_data {
    rm -rf $DATADIR/*
    rm logs/*
}

./02-stop.sh || echo ok
sleep 2
del_data
