#!/usr/bin/env -S bash

set -xueo pipefail

source 00-dir.sh

DIR=$(dirname $(readlink -f $0))
JAVA_HOME=~/prg/java-23
DATADIR=$HOME/kafka-logs
mkdir -p $DATADIR
mkdir -p $DIR/logs

# Update log.dirs and kafka.logs.dir in cluster.cfg
sed -i "s|^log.dirs=.*|log.dirs=${DATADIR}|g" cluster.cfg
sed -i "s|^kafka.logs.dir=.*|kafka.logs.dir=${DIR}/logs/|g" cluster.cfg

if [ ! -f $DATADIR/meta.properties ]; then
    ~/prg/kafka/bin/kafka-storage.sh format --config cluster.cfg --cluster-id asdf
fi

export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:$DIR/log4j.properties -Dkafka.logs.dir=$DIR/logs"
export KAFKA_HEAP_OPTS=" -Xms2g -Xmx2g "
export LOG_DIR="$DIR/logs"
tmux new -d -s kafka \
    -e KAFKA_LOG4J_OPTS="$KAFKA_LOG4J_OPTS" \
    -e LOG_DIR="$LOG_DIR" \
    -e KAFKA_HEAP_OPTS="$KAFKA_HEAP_OPTS" \
    "$HOME/prg/kafka/bin/kafka-server-start.sh cluster.cfg"
