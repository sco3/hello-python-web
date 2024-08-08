///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"log"
	"runtime"
	"strconv"
	"sync"
	"time"

	"github.com/nats-io/nats.go"
)

func call(nc *nats.Conn, num int, results chan int, wg *sync.WaitGroup, mu *sync.Mutex, i2 int, i *[]int) {
	defer wg.Done()
	const subj string = "square"
	var sNum string = strconv.Itoa(num)
	var res *nats.Msg
	res, _ = nc.Request(subj, []byte(sNum), time.Hour)
	sNum = string(res.Data)
	var outNum int
	outNum, _ = strconv.Atoi(sNum)
	mu.Lock()
	(*i)[i2] = outNum
	mu.Unlock()
	//results <- outNum
	//mu.Store(num, outNum)

}

func aggregate(num int, nc *nats.Conn) []int {
	var wg sync.WaitGroup
	wg.Add(num)
	var resChannels chan int = make(chan int, num)
	var mu sync.Mutex
	var a []int = make([]int, num)
	for i := 0; i < num; i++ {
		go call(nc, i+1, resChannels, &wg, &mu, i, &a)
	}
	wg.Wait()
	close(resChannels)
	/*
		for i := 0; i < num; i++ {
			if value, ok := mu.Load(i); ok {
				a[i] = value.(int)
			}
		}
	*/
	/*
		var i int = 0
		for r := range resChannels {
			a[i] = r
			i++
		}
	*/
	//sort.Ints(a)
	//fmt.Printf("%v\n", a)
	return a
}

func main() {
	runtime.GOMAXPROCS(1)
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

	//fmt.Printf("Took: %#0.4f ms %v", 1000*dur.Seconds(), results)
	fmt.Printf("Took: %v %v", dur, results)

}
