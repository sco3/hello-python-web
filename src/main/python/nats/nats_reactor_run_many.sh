


DEFAULT="1000"

n="${1:-$DEFAULT}"


for (( i=0; i<$n; i++)); do
    time ./nats_reactor_rr.py &
done

while true; do 
    n=$(ps -aef | grep nats_reactor_rr.py | grep -v grep | wc -l )
   if [[ "$n" == "0" ]]; then
      break
   fi
   echo $n
   sleep 1
done




