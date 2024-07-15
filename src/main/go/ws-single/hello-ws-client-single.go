package main

import (
    "fmt"
    "log"
    "time"

    "github.com/gorilla/websocket"
)

func main() {
    // Define the WebSocket server address
    serverURL := "ws://localhost:8081"

    // Create a new WebSocket connection
    dialer := websocket.Dialer{}
    conn, _, err := dialer.Dial(serverURL, nil)
    if err != nil {
        log.Fatal("Error connecting to WebSocket server:", err)
    }
    defer conn.Close()

    // Set a 1-second write deadline (optional)
    conn.SetWriteDeadline(time.Now().Add(1 * time.Second))

    // Send a message to the server
    err = conn.WriteMessage(websocket.TextMessage, []byte("Hello from Go client"))
    if err != nil {
        log.Fatal("Error writing to WebSocket:", err)
    }

    // Set a 1-second read deadline (optional)
    conn.SetReadDeadline(time.Now().Add(1 * time.Second))

    // Read the server's response
    _, message, err := conn.ReadMessage()
    if err != nil {
        log.Fatal("Error reading from WebSocket:", err)
    }

    // Print the server's response
    fmt.Printf("Received from server: %s\n", message)
}