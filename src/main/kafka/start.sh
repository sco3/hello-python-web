#!/usr/bin/env -S bash

DIR=$(dirname $(readlink -f $0))
JAVA_HOME=~/prg/java-21
DATADIR=$HOME/kafka-logs
mkdir -p $DATADIR
mkdir -p $DIR/logs




# Update log.dirs and kafka.logs.dir in cluster.cfg
sed -i "s|^log.dirs=.*|log.dirs=${DATADIR}|g" cluster.cfg
sed -i "s|^kafka.logs.dir=.*|kafka.logs.dir=${DIR}/logs/|g" cluster.cfg


if [ ! -f $DATADIR/meta.properties ] ; then 
    ~/prg/kafka/bin/kafka-storage.sh format --config cluster.cfg --cluster-id asdf
fi

export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:$DIR/log4j.properties -Dkafka.logs.dir=$DIR/logs"
export LOG_DIR="$DIR/logs"
~/prg/kafka/bin/kafka-server-start.sh cluster.cfg
