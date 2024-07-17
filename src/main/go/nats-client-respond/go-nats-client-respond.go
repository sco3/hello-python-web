package main

import (
    //"fmt"
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

    // Start time for the program
    startTime := time.Now()

    for {
	// Check if 10 seconds have passed
	if time.Since(startTime) > 10*time.Second {
	    break
	}

	id := uuid.New().String()
	resSubj := "res." + id
	reqSubj := "req." + id

	// Create a channel to signal message reception
	received := make(chan *nats.Msg)

	// Subscribe to the response subject asynchronously
	sub, err := nc.Subscribe(resSubj, func(msg *nats.Msg) {
	    received <- msg // Signal message reception
	})
	if err != nil {
	    log.Fatal(err)
	}

	// Publish the request with the reply subject
	err = nc.PublishRequest(reqSubj, resSubj, []byte("Hello, world!"))
	if err != nil {
	    log.Fatal(err)
	}

	// Wait for the response
	select {
	case _ = <-received:
	    //fmt.Printf("Received response: %s\n", string(msg.Data))
	}

	// Unsubscribe from the subject
	sub.Unsubscribe()
    }
}
