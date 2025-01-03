

pkill nats-server
rm -rf ~/nats-logs

./tmux-run-nats-js-cluster-no-pass.go


#sleep 4
#./stream.sh
