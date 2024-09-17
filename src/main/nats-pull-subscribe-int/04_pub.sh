
source 04_count.sh

for i in $(seq 1 $COUNT); do
   nats pub subject_int1 "asdf-jkl-asdf-$i"
   nats pub subject_int2 "asdf-jkl-asdf-$i"
done