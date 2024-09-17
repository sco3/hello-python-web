nats consumer add stream_retention_int consumer_int1  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_int1" \
   --max-deliver=-1 \
   --defaults


nats consumer add stream_retention_int consumer_int2  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_int2" \
   --max-deliver=-1 \
   --defaults

