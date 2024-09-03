nats consumer add stream_retention_work consumer_work1  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_work1" \
   --max-deliver=-1 \
   --defaults


nats consumer add stream_retention_work consumer_work2  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_work2" \
   --max-deliver=-1 \
   --defaults

