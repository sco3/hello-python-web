

source 00-dir.sh

set -xueo pipefail

function del_data {
    rm -rf $DATADIR/*
    rm logs/*
}

#if [ "$(./02-stop.sh)" == "No kafka server to stop" ] ; then
#       del_data
#fi


if [ -f $DATADIR/.kafka_cleanshutdown ] ; then
    del_data
else
    echo kafka is running probably or was not started
fi