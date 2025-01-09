

./02-stop.sh
sleep 1
./03-clean.sh
./01-start.sh

sleep 1
./test-topic.sh
sleep 1

tmux new -d -s sub ./test-sub.sh $1
tmux new -d -s pub ./test-pub.sh $1

set -xueo pipefail

while true; do
    pubout="test-pub.sh.out.$1.msgs"
    subout="test-sub.sh.out.$1.msgs"

    # Check if both files exist
    if [ -f "$pubout" ] && [ -f "$subout" ]; then
        OUT="$0.out.$1.msgs"

        # Remove existing output file if it exists
        rm -rf "$OUT"

        # Append the first column of $pubout to the output file
        awk '{print $1}' "$pubout" >>"$OUT"

        # Append the last line of $subout to the output file
        tail -n 1 "$subout" >>"$OUT"
        
        break
    fi

    # Optional: Add a small sleep to avoid overloading the CPU in an infinite loop
    sleep 1
done
