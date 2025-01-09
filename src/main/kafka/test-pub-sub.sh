
./02-stop.sh
sleep 1
./03-clean.sh
./01-start.sh

sleep 1
./test-topic.sh
sleep 1



tmux new -d -s sub ./test-sub.sh $1
tmux new -d -s pub ./test-pub.sh $1
