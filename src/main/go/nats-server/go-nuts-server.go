package main

import (
	"log"

	"github.com/nats-io/nats.go"
)

const hello string = "Hello, world!\n"

func main() {
	var hello_bytes []byte = []byte(hello)
	// Connect to NATS server
	opts := nats.Options{
		Servers: []string{
			"nats://127.0.0.1:4222", //
			"nats://127.0.0.1:4223", //
			"nats://127.0.0.1:4224", //
		},
		User:     "sys",
		Password: "pass",
	}
	// nc, err := nats.Connect( //
	// 	"nats://127.0.0.1:4222,nats://127.0.0.1:4223,nats://127.0.0.1:4224", //
	// 	Options.User(), // change &opts to opts
	// )
	nc, err := opts.Connect()
	if err != nil {
		log.Fatal(err)
	}
	defer nc.Close()

	// Subscribe to the "ping" subject
	nc.Subscribe("req.*", func(m *nats.Msg) {
		//fmt.Printf("Received: %s %s\n", string(m.Data), m.Subject)
		nc.Publish("res."+m.Subject[4:], hello_bytes)
	})

	// Keep the connection alive
	select {}
}
