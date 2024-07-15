package main

import (
	"fmt"
	"sync/atomic"
	"time"

	"github.com/gorilla/websocket"
)

var addr = "ws://localhost:8081/ws" // Change to your WebSocket server address
var parallel = 2
var threads = 2

// Function to handle a single WebSocket connection
func handleConnection(id *int64, t_duration *int64, t_requests *int64, t_bytes *int64) {
	atomic.AddInt64(id, 1)
	defer atomic.AddInt64(id, -1)

	// Connect to WebSocket server
	c, _, err := websocket.DefaultDialer.Dial(addr, nil)
	if err != nil {
		fmt.Printf("Connection %d: error during connection: %v\n", atomic.LoadInt64(id), err)
		return
	}
	defer c.Close()

	// Send a message to the server
	message := "Hello, Server!"
	start := time.Now() // Record time before sending
	err = c.WriteMessage(websocket.TextMessage, []byte(message))
	if err != nil {
		fmt.Printf("Connection %d: error sending message: %v\n", id, err)
		return
	}

	// Wait for the response
	_, response, err := c.ReadMessage()
	if err != nil {
		fmt.Printf("Connection %d: error reading message: %v\n", id, err)
		return
	}
	end := time.Now() // Record time after receiving

	// Calculate RTT
	rtt := end.Sub(start)

	//fmt.Printf("Connection %d: received message from server: %s\n", id, string(response))

	dataSize := float64(len(message) + len(response))
	atomic.AddInt64(t_duration, int64(rtt.Nanoseconds()))
	atomic.AddInt64(t_requests, 1)
	atomic.AddInt64(t_bytes, int64(dataSize))

	//fmt.Printf("Connection %d: RTT = %v, Throughput = %f MB/s\n", id, rtt, throughput)

}

// Function to open 200 WebSocket connections
func openSomeConnections(t_duration *int64, t_requests *int64, t_bytes *int64) {
	count := int64(0)
	for {
		if atomic.LoadInt64(&count) < 200 {
			go handleConnection(&count, t_duration, t_requests, t_bytes)
		}
	}

}

func main() {
	t_duration := int64(0)
	t_requests := int64(0)
	t_bytes := int64(0)
	start := time.Now()
	fmt.Printf("Start with: %v threads %v parallel requests\n", threads, parallel)
	for i := 0; i < 2; i++ {
		go openSomeConnections(&t_duration, &t_requests, &t_bytes)
	}

	duration := time.Duration(0)
	var end time.Time
	for {
		end = time.Now() // Record time after receiving
		duration = end.Sub(start)
		if duration > 10*time.Second {
			break
		}
	}

	avg := float64(t_duration) / float64(t_requests) / 1000_000
	trhougput := float64(t_bytes) / float64(duration.Seconds()) / 1024 / 1024
	fmt.Printf("Duration: %v\n", duration)
	fmt.Printf("Requests sent/received: %v Avg: %v ms thoughput: %v mb/s\n",
		t_requests, avg, trhougput,
	)
}
