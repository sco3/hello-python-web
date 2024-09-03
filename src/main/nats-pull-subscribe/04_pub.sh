
for i in $(seq 1 10); do
   nats pub subject_limits "asdf$i"
done