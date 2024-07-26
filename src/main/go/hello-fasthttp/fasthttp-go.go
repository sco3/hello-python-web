///usr/bin/true; exec /usr/bin/env go run "$0" "$@"

package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/valyala/fasthttp"
)

func main() {
	const sqPrefix = "/square/"
	const sqPrefixLen = len(sqPrefix)
	// Define a request handler function
	requestHandler := func(ctx *fasthttp.RequestCtx) {
		path := string(ctx.Path())
		if strings.HasPrefix(path, sqPrefix) {
			sNum := path[sqPrefixLen:]
			num, _ := strconv.Atoi(sNum)
			fmt.Fprint(ctx, num*num)
		} else {
			fmt.Fprint(ctx, "Hello, world!\n")
		}

	}

	if err := fasthttp.ListenAndServe(":8000", requestHandler); err != nil {
		fmt.Printf("Error in ListenAndServe: %s\n", err)
	}
}
