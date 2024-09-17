
for i in $(seq 1 1); do
   nats pub subject_limits "asdf-jkl-asdf-$i"
done