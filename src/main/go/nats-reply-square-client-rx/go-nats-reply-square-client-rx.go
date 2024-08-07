///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/reactivex/rxgo/v2"

	"strconv"

	"github.com/nats-io/nats.go"
)

const subj = "square"

func call(nc *nats.Conn, num int) int {
	bytes := toBytes(num)
	res, _ := nc.Request(subj, bytes, time.Hour)
	bytes = res.Data
	outNum := fromBytes(bytes)
	return outNum
}

func call2(nc *nats.Conn, bytes []byte) []byte {
	res, _ := nc.Request(subj, bytes, time.Hour)
	bytes = res.Data
	return bytes
}

func fromBytes(bytes []byte) int {
	outNum, _ := strconv.Atoi(string(bytes))
	return outNum
}

func toBytes(num int) []byte {
	bytes := []byte(strconv.Itoa(num))
	return bytes
}

func aggregate(num int, nc *nats.Conn) []int {
	var result = make([]int, num)

	observable := rxgo.Range(1, num).
		Map( //
			func(ctx context.Context, i interface{}) (interface{}, error) {
				return toBytes(i.(int)), nil
			},
		).   //
		Map( //
			func(_ context.Context, item interface{}) (interface{}, error) {
				return call2(nc, item.([]byte)), nil
			}, //
		). //
		Map(func(ctx context.Context, i interface{}) (interface{}, error) {
			return fromBytes(i.([]byte)), nil
		})
	i := 0
	for item := range observable.Observe() {
		n := item.V.(int)
		result[i] = n
		i++
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
