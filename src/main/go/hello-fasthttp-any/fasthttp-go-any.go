///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"github.com/valyala/fasthttp"
	"os"
)

func main() {
	var port string = "8000"
	msg := "ok"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	if (len(os.Args)) > 2 {
		msg = os.Args[2]
	}
	fmt.Printf("Port: %v message: %v\n", port, msg)

	// Define a request handler function
	requestHandler := func(ctx *fasthttp.RequestCtx) {
		fmt.Fprint(ctx, msg)
	}

	if err := fasthttp.ListenAndServe(":"+port, requestHandler); err != nil {
		fmt.Printf("Error in ListenAndServe: %s\n", err)
	}
}
