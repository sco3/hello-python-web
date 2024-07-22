///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"github.com/nats-io/nats.go"
	"log"
	"sync/atomic"
	"time"
)

const hello string = "Hello, world!\n"
const delay int64 = 12 * int64(time.Second/time.Nanosecond)

func print_stats(count_ref *int64, first_ref *int64, last_ref *int64, byte_count_ref *int64) {
	for {
		first := atomic.LoadInt64(first_ref)
		if first > 0 {
			now := int64(time.Now().UTC().UnixNano())
			passed_ns := now - first
			var old_byte_count int64 = atomic.LoadInt64(byte_count_ref)
			if (passed_ns > delay) && (old_byte_count > 0) {
				last := atomic.SwapInt64(last_ref, 0)
				atomic.StoreInt64(last_ref, 0)
				atomic.StoreInt64(first_ref, 0)
				old_byte_count = atomic.SwapInt64(byte_count_ref, 0)
				dur := float64((last-first)*int64(time.Nanosecond)) / float64(time.Second)
				count := atomic.SwapInt64(count_ref, 0)
				fmt.Printf("Duration: %v s requests: %v bytes: %v throughput: %v mb/s\n",
					dur, count, old_byte_count,
					float64(old_byte_count)/1024/1024/float64(dur),
				)
			}
		}
		time.Sleep(1 * time.Second)
	}

}

func main() {

	var hello_bytes []byte = []byte(hello)
	opts := nats.Options{
		Servers: []string{
			"nats://127.0.0.1:4222", //
			"nats://127.0.0.1:4223", //
			"nats://127.0.0.1:4224", //
		},
		User:     "sys",
		Password: "pass",
	}
	nc, err := opts.Connect()
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	subj := "req.*"

	var first int64 = int64(0)
	var last int64 = int64(0)
	var byte_count int64 = int64(0)
	var count int64 = int64(0)

	nc.QueueSubscribe(subj, "worker", func(m *nats.Msg) {
		atomic.AddInt64(&count, 1)
		now := int64(time.Now().UTC().UnixNano())
		if atomic.LoadInt64(&first) == 0 {
			atomic.StoreInt64(&first, now)
		}
		atomic.StoreInt64(&last, now)
		atomic.AddInt64(&byte_count, int64(m.Size()))
		m.Respond(hello_bytes)
		if err != nil {
			log.Printf("Failed to respond to message: %v", err)
		}
	})
	println("listening:", subj)
	go print_stats(&count, &first, &last, &byte_count)
	// Keep the connection alive
	select {}
}
