

port=9092
host=$(

~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$port --create --topic asdf --config max.message.bytes=1048664
~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$port --list
~/prg/kafka/bin/kafka-topics.sh  --bootstrap-server localhost:$port --describe --topic asdf

