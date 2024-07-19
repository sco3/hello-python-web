///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"log"
	"time"

	"github.com/google/uuid"
	"github.com/nats-io/nats.go"
)

func main() {
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

	hello := []byte("Hello, world!\n")
	// Start time for the program
	startTime := time.Now()
	traffic := 0
	count := 0

	for {
		// Check if 10 seconds have passed
		if time.Since(startTime) > 10*time.Second {
			break
		}

		id := uuid.New().String()
		reqSubj := "req." + id

		// Create a channel to signal message reception

		resp, err := nc.Request(reqSubj, hello, 4*time.Second)
		if err != nil {
			log.Fatal(err)
		} else {
			traffic += len(resp.Data) + len(hello)
			count++
		}
	}
	endTime := time.Now()
	dur := endTime.Sub(startTime)
	fmt.Printf("Time taken: %.3f\n", dur.Seconds())
	fmt.Printf("Requests: %v %.3f r/s\n", count, float64(count)/dur.Seconds())
	mbs := (float64(traffic) / (1024 * 1024)) / dur.Seconds()
	expected := count * 2 * len("Hello, world!\n")
	fmt.Printf("Traffic: %v/%v bytes %.3f mb/s\n", traffic, expected, mbs)
}
