nats consumer add stream_retention_limits consumer_limits1  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_limits" \
   --max-deliver=-1 \
   --defaults


nats consumer add stream_retention_limits consumer_limits2  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_limits" \
   --max-deliver=-1 \
   --defaults

