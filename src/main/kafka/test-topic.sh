
set -xueo pipefail
source ./00-sizes.sh


~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$PORT \
    --create \
    --topic asdf \
    --partitions 1 \
    --config retention.ms=180000 max.message.bytes=1048664

~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$PORT --list
~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$PORT --describe --topic asdf

