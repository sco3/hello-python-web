///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"log"

	"strconv"

	"github.com/nats-io/nats.go"
)

func main() {

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

	subj := "square"

	nc.QueueSubscribe(subj, "worker", func(m *nats.Msg) {
		i, _ := strconv.Atoi(string(m.Data))
		i = i * i
		hello_bytes := []byte(strconv.Itoa(i))
		err = m.Respond(hello_bytes)
		if err != nil {
			log.Printf("Failed to respond to message: %v", err)
		}
	})
	println("listening:", subj)
	// Keep the connection alive
	select {}
}
