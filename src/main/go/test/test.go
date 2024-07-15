package main

import (
	"fmt"
	"sync"
	"time"
)

func run(wg *sync.WaitGroup, ri int) {

	defer wg.Done()
	for i := 0; i < 10; i++ {
		fmt.Printf("run %d %d\n", ri, i)
		time.Sleep(1 * time.Second)
	}

}

func main() {
	var wg sync.WaitGroup
	start := time.Now()

	fmt.Printf("start\n")
	wg.Add(1)
	go run(&wg, 0)
	for {
		current := time.Now()
		if current.Sub(start) > 5*time.Second {
			break
		}
	}
	fmt.Printf("stop\n")
}
