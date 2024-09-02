




for i in $(seq 1 10); do
   nats pub subj_lim "asdf$i"
done