package main

import (
	"fmt"
	"log"

	"github.com/nats-io/nats.go"
)

const hello string = "Hello, world!\n"

func main() {
	var hello_bytes []byte = []byte(hello)
	// Connect to NATS server
	nc, err := nats.Connect(nats.DefaultURL)
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	// Subscribe to the "ping" subject
	nc.Subscribe("req.*", func(m *nats.Msg) {
		fmt.Printf("Received: %s %s\n", string(m.Data), m.Subject)
		nc.Publish("res."+m.Subject[4:], hello_bytes)
	})

	// Keep the connection alive
	select {}
}
