

port=9092
host=$(rpk cluster info -b | tail -n 1 | awk '{print $2}')
port=$(rpk cluster info -b | tail -n 1 | awk '{print $3}')


~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server $host:$port --create --topic asdf --config max.message.bytes=1048664
~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server $host:$port --list
~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server $host:$port --describe --topic asdf

