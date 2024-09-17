
for i in $(seq 1 $(cat 04_count.txt)); do
   nats pub subject_limits "asdf-jkl-asdf-$i" --server nats://127.0.0.1:4224
done