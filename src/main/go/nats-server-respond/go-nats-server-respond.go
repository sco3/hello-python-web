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

	nc.Subscribe("req.*", func(m *nats.Msg) {
		//nc.Publish("res."+m.Subject[4:], hello_bytes)
		m.Respond(hello_bytes)
		if err != nil {
			log.Printf("Failed to respond to message: %v", err)
		}
	})

	// Keep the connection alive
	select {}
}
