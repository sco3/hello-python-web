


~/prg/confluent/bin/kafka-topics --bootstrap-server localhost:33001 --create --topic asdf --config max.message.bytes=1048664
~/prg/confluent/bin/kafka-topics --bootstrap-server localhost:33001 --list
~/prg/confluent/bin/kafka-topics --bootstrap-server localhost:33001 --describe --topic asdf

