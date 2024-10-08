///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"log"
	"time"

	"strconv"

	"github.com/nats-io/nats.go"
)

func call(nc *nats.Conn, num int) int {
	var subj string = "square"

	var sNum string = strconv.Itoa(num)
	var res *nats.Msg
	res, _ = nc.Request(subj, []byte(sNum), time.Hour)
	sNum = string(res.Data)
	var outNum int
	outNum, _ = strconv.Atoi(sNum)
	return outNum
}

func aggregate(num int, nc *nats.Conn) []int {
	var result = make([]int, num)


	var i int
	for i = 0; i < num; i++ {
		var outNum = call(nc, i+1)
		result[i] = outNum
	}
	return result
}

func main() {
	const nTests int = 1000
	const number int = 1000
	var start time.Time
	start = time.Now()

	var opts = nats.Options{
		Servers: []string{
			"nats://127.0.0.1:4222", //
			"nats://127.0.0.1:4223", //
			"nats://127.0.0.1:4224", //
		},
		User:     "sys",
		Password: "pass",
	}
	var nc, err = opts.Connect()
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	var results map[int]struct{} = make(map[int]struct{})
	for i := 0; i < nTests; i++ {
		result := aggregate(number, nc)
		results[len(result)] = struct{}{}
	}

	var dur time.Duration
	dur = time.Now().Sub(start)

	fmt.Printf("Took: %#0.4f ms %v", 1000*dur.Seconds(), results)

}
