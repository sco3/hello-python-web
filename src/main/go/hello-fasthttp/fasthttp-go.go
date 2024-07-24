///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"

	"github.com/valyala/fasthttp"
)

func main() {
	// Define a request handler function
	requestHandler := func(ctx *fasthttp.RequestCtx) {
		fmt.Fprint(ctx, "Hello, world!\n")
	}

	// Start the server on port 8080
	if err := fasthttp.ListenAndServe(":8000", requestHandler); err != nil {
		fmt.Printf("Error in ListenAndServe: %s\n", err)
	}
}
