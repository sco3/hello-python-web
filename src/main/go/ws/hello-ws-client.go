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
var message = "Hello, world!\n"

func handleConnection(count *int64, stats *Stats) {
	defer wg.Done()
	// Connect to WebSocket server
	c, _, err := websocket.DefaultDialer.Dial(addr, nil)
	if err != nil {
		fmt.Printf("Error during connection: %v\n", err)
		return
	}
	defer c.Close()
	defer atomic.AddInt64(count, -1)

	start := time.Now() // Record time before sending
	err = c.WriteMessage(websocket.TextMessage, []byte(message))
	if err != nil {
		fmt.Printf("Error sending message: %v\n", err)
		return
	}

	_, response, err := c.ReadMessage()
	if err != nil {
		fmt.Printf("Error reading message: %v\n", err)
		return
	}
	end := time.Now() // Record time after receiving
	rtt := end.Sub(start)

	atomic.AddInt64(&stats.dur, int64(rtt.Nanoseconds()))
	atomic.AddInt64(&stats.cnt, 1)
	atomic.AddInt64(&stats.rcv, int64(len(response)))
	atomic.AddInt64(&stats.snt, int64(len(message)))
}

// Function to open 200 WebSocket connections
func openSomeConnections(id int, stats *Stats) {
	defer wg.Done()
	count := int64(0)
	for atomic.LoadInt64(&stop_flag) == 0 {
		if atomic.LoadInt64(&count) < int64(parallel) {
			atomic.AddInt64(&count, 1)
			wg.Add(1)
			go handleConnection(&count, stats)
		}
	}
	for atomic.LoadInt64(&count) > 0 {
		fmt.Printf("Thread: %v Count: %v\n", id, atomic.LoadInt64(&count))
		time.Sleep(1000 * time.Millisecond)
	}
	fmt.Printf("Thread: %v Count: %v\n", id, atomic.LoadInt64(&count))
}

type Stats struct {
	dur int64
	cnt int64
	snt int64
	rcv int64
}

func main() {
	stats := Stats{
		dur: 0,
		cnt: 0,
		snt: 0,
		rcv: 0,
	}

	start := time.Now()
	fmt.Printf("Start with: %v threads %v parallel requests\n", threads, parallel)
	for i := 0; i < 2; i++ {
		wg.Add(1)
		go openSomeConnections(i, &stats)
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

	avg := float64(stats.dur) / float64(stats.cnt) / 1000_000
	//tsnt := float64(stats.snt) / float64(stats.dur) / 1024 / 1024
	//trcv := float64(stats.rcv) / float64(stats.dur) / 1024 / 1024
	fmt.Printf("Duration: %v\n", duration)
	fmt.Printf("Requests sent/received: %v Avg: %v ms thoughput: %v/%v bytes expected: %v\n",
		stats.cnt, avg, stats.snt, stats.rcv, int64(len(message))*stats.cnt,
	)
}
