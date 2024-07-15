package main

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gorilla/websocket"
)

var addr = "ws://localhost:8081/ws" // Change to your WebSocket server address
var parallel = int64(200)
var threads = 2
var wg = sync.WaitGroup{}
var stop_flag = int64(0)

// Function to handle a single WebSocket connection
func handleConnection(count *int64, t_duration *int64, t_requests *int64, t_bytes *int64) {
	defer wg.Done()
	// Connect to WebSocket server
	c, _, err := websocket.DefaultDialer.Dial(addr, nil)
	if err != nil {
		fmt.Printf("Error during connection: %v\n", err)
		return
	}
	defer c.Close()
	defer atomic.AddInt64(count, -1)

	// Send a message to the server
	message := "Hello, Server!"
	start := time.Now() // Record time before sending
	err = c.WriteMessage(websocket.TextMessage, []byte(message))
	if err != nil {
		fmt.Printf("Error sending message: %v\n", err)
		return
	}

	// Wait for the response
	_, response, err := c.ReadMessage()
	if err != nil {
		fmt.Printf("Error reading message: %v\n", err)
		return
	}
	end := time.Now() // Record time after receiving

	// Calculate RTT
	rtt := end.Sub(start)

	dataSize := float64(len(message) + len(response))
	atomic.AddInt64(t_duration, int64(rtt.Nanoseconds()))
	atomic.AddInt64(t_requests, 1)
	atomic.AddInt64(t_bytes, int64(dataSize))

	//fmt.Printf("Connection %d: RTT = %v, Throughput = %f MB/s\n", id, rtt, throughput)

}

// Function to open 200 WebSocket connections
func openSomeConnections(id int, t_duration *int64, t_requests *int64, t_bytes *int64) {
	count := int64(0)
	for atomic.LoadInt64(&stop_flag) == 0 {
		if atomic.LoadInt64(&count) < int64(parallel) {
			atomic.AddInt64(&count, 1)
			wg.Add(1)
			go handleConnection(&count, t_duration, t_requests, t_bytes)
		}
	}
	for atomic.LoadInt64(&count) > 0 {
		fmt.Printf("Thread: %v Count: %v\n", id, atomic.LoadInt64(&count))
		time.Sleep(100 * time.Millisecond)
	}
	fmt.Printf("Thread: %v Count: %v\n", id, atomic.LoadInt64(&count))
}

func main() {

	t_duration := int64(0)
	t_requests := int64(0)
	t_bytes := int64(0)
	start := time.Now()
	fmt.Printf("Start with: %v threads %v parallel requests\n", threads, parallel)
	for i := 0; i < 2; i++ {
		go openSomeConnections(i, &t_duration, &t_requests, &t_bytes)
	}

	duration := time.Duration(0)
	var end time.Time
	for {
		end = time.Now() // Record time after receiving
		duration = end.Sub(start)
		if duration > 10*time.Second {
			atomic.AddInt64(&stop_flag, 1)
			break
		}
		time.Sleep(time.Millisecond)
	}
	wg.Wait()

	avg := float64(t_duration) / float64(t_requests) / 1000_000
	trhougput := float64(t_bytes) / float64(duration.Seconds()) / 1024 / 1024
	fmt.Printf("Duration: %v\n", duration)
	fmt.Printf("Requests sent/received: %v Avg: %v ms thoughput: %v mb/s\n",
		t_requests, avg, trhougput,
	)
}
