nats stream add stream_retention_work \
  --subjects "subject_work1,subject_work2" \
  --storage file \
  --retention work \
  --max-msgs=70000000 \
  --max-age="7d" \
  --max-bytes=20g \
  --ack \
  --discard=old \
  --defaults