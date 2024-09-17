///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"net/http"
)

func main() {

	var maxGoroutines int = 40
	fmt.Printf("Concurrency: %d\n", maxGoroutines)
	var semaphore chan struct{} = make(chan struct{}, maxGoroutines)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		semaphore <- struct{}{}
		fmt.Fprintf(w, "Hello, world!: %s\n", r.URL.Path)
		<-semaphore
	})

	http.ListenAndServe(":8000", nil)
}
