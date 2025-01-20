#!/usr/bin/env -S bash

set -xueo pipefail

./01-reset.sh

source 00-sizes.sh

set -xueo pipefail

./07.01_python_json.py --nats_url nats://localhost:4222 --subject limi_sujb --message_size $SIZE --num_messages $NUM | tee $0.out.$SIZE 

#--nats_url nats://localhost:4222 \
#    --subject limi_sujb \
#    --message_size $SIZE \
#    --num_messages $NUM | tee $0.out.$SIZE
