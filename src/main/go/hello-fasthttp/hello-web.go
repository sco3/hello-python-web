///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/valyala/fasthttp"
)

func main() {
	requestHandler := func(ctx *fasthttp.RequestCtx) {
			fmt.Fprint(ctx, "Hello, world!\n")
	}

	if err := fasthttp.ListenAndServe(":8000", requestHandler); err != nil {
		log.Fatalf("Error in ListenAndServe: %s", err)
	}
}
