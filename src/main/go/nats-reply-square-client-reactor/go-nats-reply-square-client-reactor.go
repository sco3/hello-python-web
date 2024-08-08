///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/jjeffcaii/reactor-go"
	"github.com/jjeffcaii/reactor-go/flux"
	"github.com/jjeffcaii/reactor-go/scheduler"

	"strconv"

	"github.com/nats-io/nats.go"
)

const subj = "square"

func handleResult(nc *nats.Conn, bytes []byte, result chan<- int) {
	var res *nats.Msg
	res, _ = nc.Request(subj, bytes, time.Hour)
	bytes = res.Data
	outNum := fromBytes(bytes)
	result <- outNum

}

func call(nc *nats.Conn, num int) int {
	var bytes []byte = toBytes(num)

	result := make(chan int)
	go handleResult(nc, bytes, result)

	outNum := <-result
	return outNum
}

/*
func _call2(nc *nats.Conn, bytes []byte) []byte {
	res, _ := nc.Request(subj, bytes, time.Hour)
	bytes = res.Data
	return bytes
}
*/

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
	var su reactor.Subscription
	done := make(chan struct{})
	i := 0
	flux.Range(1, num).
		Map(func(input reactor.Any) (reactor.Any, error) {
			output := call(nc, input.(int))
			return output, nil
		}).
		SubscribeOn(scheduler.Single()).
		Subscribe(context.Background(),
			reactor.OnSubscribe(
				func(_ context.Context, s reactor.Subscription) {
					su = s
					s.Request(1)
				}),
			reactor.OnNext(func(v reactor.Any) error {
				result[i] = v.(int)
				i++
				su.Request(1)
				return nil
			}),
			reactor.OnComplete(func() {
				close(done)
			}),
		)
	<-done
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
		//fmt.Printf("Result: %v\n", result)
		results[len(result)] = struct{}{}
	}

	var dur time.Duration
	dur = time.Now().Sub(start)

	fmt.Printf("Took: %#0.4f ms %v", 1000*dur.Seconds(), results)

}
