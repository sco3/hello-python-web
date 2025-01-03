

source 00-dir.sh

set -xueo pipefail

if [ -f $DATADIR/.kafka_cleanshutdown ] ; then

    rm -rf $DATADIR/*
    rm logs/*
else
    echo kafka is running probably or was not started
fi