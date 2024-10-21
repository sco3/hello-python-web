///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"github.com/valyala/fasthttp"
	"os"
)

func main() {
	var port string = "8000"
	var msg string = "ok"
	if len(os.Args) > 1 {
		port = os.Args[1]
	}
	if (len(os.Args)) > 2 {
		msg = os.Args[2]
	}
	fmt.Printf("Port: %v message: %v\n", port, msg)

	// Define a request handler function
	var last_ts int = int(ctx.Time().Unix())
	requestHandler := func(ctx *fasthttp.RequestCtx) {
		var now int = int(ctx.Time().Unix())
		var inactivity int = now - last_ts
		last_ts = now
		path := string(ctx.Path())
		// fmt.Printf("Path: %v inactivity: %d\n", path, inactivity)
		if path == "/" {
			ctx.SetContentType("application/json")
			fmt.Fprintf(ctx, "{\"inactive_seconds\":%d}", inactivity)
		} else {
			fmt.Fprint(ctx, msg)
		}
	}

	if err := fasthttp.ListenAndServe(":"+port, requestHandler); err != nil {
		fmt.Printf("Error in ListenAndServe: %s\n", err)
	}
}
