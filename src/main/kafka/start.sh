


sed  "s!log.dirs=.+$!log.dirs=$HOME/kafka-logs" cluster.cfg


~/prg/confluent/bin/kafka-storage format --config cluster.cfg --cluster-id asdf


#~/prg/confluent/bin/kafka-server-start cluster.cfg
