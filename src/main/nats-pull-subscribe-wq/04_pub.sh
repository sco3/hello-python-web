
for i in $(seq 1 10); do
   nats pub subject_work1 "asdf$i"
done