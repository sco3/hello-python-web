nats consumer add  stream_lim cons_lim2  \
   --pull \
   --deliver all \
   --ack explicit \
   --filter "subj_lim"  \
   --replay instant \
   --max-pending=-1 \
   --no-headers-only \
   --defaults