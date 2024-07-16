package main

import (
	"fmt"
	"math"
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
	defer closeGracefully(c)
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
	min_rtt := atomic.LoadInt64(&stats.min_rtt)
	max_rtt := atomic.LoadInt64(&stats.max_rtt)
	if min_rtt > int64(rtt) {
		atomic.StoreInt64(&stats.min_rtt, rtt.Nanoseconds())
	}
	if max_rtt < int64(rtt) {
		atomic.StoreInt64(&stats.max_rtt, rtt.Nanoseconds())
	}

	atomic.AddInt64(&stats.dur, int64(rtt.Nanoseconds()))
	atomic.AddInt64(&stats.cnt, 1)
	atomic.AddInt64(&stats.rcv, int64(len(response)))
	atomic.AddInt64(&stats.snt, int64(len(message)))
}

func closeGracefully(c *websocket.Conn) {
	defer c.Close()
	err := c.WriteMessage(
		websocket.CloseMessage,
		websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""),
	)
	if err != nil {
		fmt.Printf("error sending close message: %v", err)
	}
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
		time.Sleep(500 * time.Millisecond)
	}
	fmt.Printf("Thread: %v Count: %v\n", id, atomic.LoadInt64(&count))
}

type Stats struct {
	min_rtt int64
	max_rtt int64
	dur     int64
	cnt     int64
	snt     int64
	rcv     int64
}

func main() {

	stats := Stats{
		min_rtt: math.MaxInt64,
		max_rtt: math.MinInt64,
		dur:     0,
		cnt:     0,
		snt:     0,
		rcv:     0,
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
		if duration >= 10*time.Second {
			atomic.AddInt64(&stop_flag, 1)
			break
		}
		time.Sleep(time.Millisecond)
	}
	wg.Wait()
	duration = end.Sub(start)

	avg_rtt := float64(stats.dur) / float64(stats.cnt) / 1000_000
	min_rtt := float64(stats.min_rtt) / 1000_000.0
	max_rtt := float64(stats.max_rtt) / 1000_000.0
	thr := float64(stats.snt+stats.rcv) / float64(duration.Seconds()) / 1024 / 1024
	fmt.Printf("Duration: %v s expected bytes: %v\n", duration.Seconds(), int64(len(message))*stats.cnt)
	fmt.Printf("Requests sent/received: %v bytes: %v/%v throughput: %v mb/s\n",
		stats.cnt, stats.snt, stats.rcv, thr,
	)
	fmt.Printf("RTT min: %v ms max: %v ms avg: %v ms\n",
		min_rtt, max_rtt, avg_rtt,
	)
}
