
for i in $(seq 1 100000); do
   nats pub subject_limits "asdf-jkl-asdf-$i"
done