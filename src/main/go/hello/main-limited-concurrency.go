///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
    "fmt"
    "net/http"
    "sync/atomic"
    "time"
)

func main() {
    var maxGoroutines int = 40
    fmt.Printf("Concurrency: %d\n", maxGoroutines)
    var semaphore chan struct{} = make(chan struct{}, maxGoroutines)

    // Declare a counter to track the number of requests
    var requestCount int64

    // Goroutine to print the counter value every 15 seconds
    go func() {
	for {
	    time.Sleep(15 * time.Second)
	    fmt.Printf("Request count: %d\n", atomic.LoadInt64(&requestCount))
	}
    }()

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
	semaphore <- struct{}{}
	// Increment the counter atomically for each request
	atomic.AddInt64(&requestCount, 1)
	fmt.Fprintf(w, "Hello, world!: %s\n", r.URL.Path)
	<-semaphore
    })

    http.ListenAndServe(":8000", nil)
}
