nats stream add stream_retention_limits \
  --subjects "subject_limits" \
  --storage file \
  --retention limits \
  --max-msgs=70000000 \
  --max-age="7d" \
  --max-bytes=20g \
  --ack \
  --discard=old \
  --defaults