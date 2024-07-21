///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"log"
	"time"

	"sync"
	"sync/atomic"

	"os"
	"strconv"

	"github.com/google/uuid"
	"github.com/nats-io/nats.go"
)

type Stats struct {
	Count int64
	Bytes int64

	group     sync.WaitGroup
	groupSize int32
	GroupStop bool
}

func (s *Stats) IncCount() {
	atomic.AddInt64(&s.Count, 1)
}
func (s *Stats) IncBytes(b int64) {
	atomic.AddInt64(&s.Bytes, b)
}
func (s *Stats) Add(i int32) {
	s.group.Add(int(i))
	atomic.AddInt32(&s.groupSize, i)
}
func (s *Stats) Done() {
	s.group.Done()
	atomic.AddInt32(&s.groupSize, -1)
}
func (s *Stats) Wait() {
	s.group.Wait()
}
func (s *Stats) GroupSize() int32 {
	return atomic.LoadInt32(&s.groupSize)
}

func call(nc *nats.Conn, stats *Stats) {
	defer stats.Done()
	hello := []byte("Hello, world!\n")
	id := uuid.New().String()
	reqSubj := "req." + id
	resSubj := "res." + id
	receiver := make(chan []byte)
	sub, err := nc.Subscribe(resSubj, func(msg *nats.Msg) {
		receiver <- msg.Data
	})
	defer sub.Unsubscribe()
	if err != nil {
		log.Fatal(err)
	}
	err = nc.PublishRequest(reqSubj, resSubj, hello)
	if err != nil {
		log.Fatal(err)
	}
	data := <-receiver

	stats.IncBytes(int64(len(data) + len(hello)))
	stats.IncCount()
}

func BenchmarkConnection(stats *Stats, limit int32) {
	opts := nats.Options{
		Servers: []string{
			"nats://127.0.0.1:4222",
			"nats://127.0.0.1:4223",
			"nats://127.0.0.1:4224",
		},
		User:     "sys",
		Password: "pass",
	}

	// Connect to NATS servers
	nc, err := opts.Connect()
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	for !stats.GroupStop {
		if stats.GroupSize() < limit {
			stats.Add(1)
			call(nc, stats)
		}
	}

}

func main() {
	conns := 1
	if len(os.Args) > 1 {
		conns, _ = strconv.Atoi(os.Args[1])
	}
	pubs := 1
	if len(os.Args) > 2 {
		pubs, _ = strconv.Atoi(os.Args[2])
	}

	fmt.Printf("Connections*Publishers: %v * %v = %v \n ", conns, pubs, conns*pubs)
	var stats Stats = Stats{
		Count: 0,
		Bytes: 0,
	}

	// Start time for the program
	startTime := time.Now()
	for i := 0; i < conns; i++ {
		go BenchmarkConnection(&stats, 400)
	}

	time.Sleep(10 * time.Second)
	stats.GroupStop = true
	stats.Wait()

	endTime := time.Now()
	dur := endTime.Sub(startTime)
	fmt.Printf("Time taken: %.3f seconds\n", dur.Seconds())
	fmt.Printf("Requests: %v %.3f r/s\n", stats.Count, float64(stats.Count)/dur.Seconds())
	mbs := (float64(stats.Bytes) / (1024 * 1024)) / dur.Seconds()
	expected := stats.Count * int64(2*len("Hello, world!\n"))
	fmt.Printf("Throughput: %v/%v bytes %.3f mb/s\n", stats.Bytes, expected, mbs)
}
