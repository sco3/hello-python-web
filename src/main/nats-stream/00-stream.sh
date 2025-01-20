nats stream add work --subjects "work_subj" --storage file --retention work --max-msgs=-1 --max-age=0 --max-bytes=-1 --ack --discard=old --defaults
nats stream add limi --subjects "limi_subj" --storage file --retention limits --max-msgs=-1 --max-age=0 --max-bytes=-1 --ack --discard=old --defaults
