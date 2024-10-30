package main

import (
	"fmt"
	"math"
	"sync"
	"sync/atomic"
	"time"

	"github.com/gorilla/websocket"
)

var port = ":8081"
var addr = "ws://localhost" + port + "/ws" // Change to your WebSocket server address
var parallel = int64(100)
var threads = 2
var wg sync.WaitGroup
var stopFlag int64 = 0
var message = "Hello, world!\n"
var treshold = 300*time.Second

type Stats struct {
	minRTT int64
	maxRTT int64
	dur    int64
	cnt    int64
	snt    int64
	rcv    int64
}

func handleConnection(stats *Stats) {
	defer wg.Done()
	// Connect to WebSocket server
	c, _, err := websocket.DefaultDialer.Dial(addr, nil)
	if err != nil {
		fmt.Printf("Error during connection: %v\n", err)
		return
	}
	defer closeGracefully(c)

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

	// Update stats
	atomic.StoreInt64(&stats.dur, atomic.LoadInt64(&stats.dur)+int64(rtt.Nanoseconds()))
	atomic.AddInt64(&stats.cnt, 1)
	atomic.AddInt64(&stats.rcv, int64(len(response)))
	atomic.AddInt64(&stats.snt, int64(len(message)))

	// Update min/max RTT
	for {
		minRTT := atomic.LoadInt64(&stats.minRTT)
		if rtt.Nanoseconds() < minRTT {
			atomic.CompareAndSwapInt64(&stats.minRTT, minRTT, rtt.Nanoseconds())
			break
		}
		break
	}
	for {
		maxRTT := atomic.LoadInt64(&stats.maxRTT)
		if rtt.Nanoseconds() > maxRTT {
			atomic.CompareAndSwapInt64(&stats.maxRTT, maxRTT, rtt.Nanoseconds())
			break
		}
		break
	}
}

func closeGracefully(c *websocket.Conn) {
	defer c.Close()
	err := c.WriteMessage(
		websocket.CloseMessage,
		websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""),
	)
	if err != nil {
		fmt.Printf("Error sending close message: %v\n", err)
	}
}

// Function to open connections
func openSomeConnections(id int, stats *Stats) {
	defer wg.Done()
	for atomic.LoadInt64(&stopFlag) == 0 {
		if atomic.LoadInt64(&stats.cnt) < parallel {
			wg.Add(1)
			go handleConnection(stats)
		}
	}
}

func main() {
	stats := Stats{
		minRTT: math.MaxInt64,
		maxRTT: math.MinInt64,
		dur:    0,
		cnt:    0,
		snt:    0,
		rcv:    0,
	}

	start := time.Now()
	fmt.Printf("Duration %v  with: %v threads %v parallel requests port: %v\n", treshold, threads, parallel, port)
	for i := 0; i < threads; i++ {
		wg.Add(1)
		go openSomeConnections(i, &stats)
	}

	duration := time.Duration(0)
	var end time.Time
	for {
		end = time.Now() // Record time after receiving
		duration = end.Sub(start)
		if duration >= treshold {
			atomic.StoreInt64(&stopFlag, 1)
			break
		}
		time.Sleep(time.Millisecond)
	}
	wg.Wait()
	duration = end.Sub(start)

	avgRTT := float64(stats.dur) / float64(stats.cnt) / 1000_000
	minRTT := float64(stats.minRTT) / 1000_000.0
	maxRTT := float64(stats.maxRTT) / 1000_000.0
	thr := float64(stats.snt+stats.rcv) / float64(duration.Seconds()) / 1024 / 1024
	fmt.Printf("Expected bytes: %v\n", int64(len(message))*stats.cnt)
	fmt.Printf("Requests sent/received: %v bytes: %v/%v throughput: %v mb/s\n",
		stats.cnt, stats.snt, stats.rcv, thr,
	)
	fmt.Printf("RTT avg: %v ms min: %v ms max: %v ms\n",
		avgRTT, minRTT, maxRTT,
	)
}
