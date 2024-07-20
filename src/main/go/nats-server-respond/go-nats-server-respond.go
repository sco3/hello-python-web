///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"log"

	"github.com/nats-io/nats.go"
)

const hello string = "Hello, world!\n"

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

	nc.Subscribe(subj, func(m *nats.Msg) {
		m.Respond(hello_bytes)
		if err != nil {
			log.Printf("Failed to respond to message: %v", err)
		}
	})
	println("listening:", subj)
	// Keep the connection alive
	select {}
}
