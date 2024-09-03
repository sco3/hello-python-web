n1ats consumer add stream_retention_limits consumer_limits2  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subject_limits"  \
   --defaults
