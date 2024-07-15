package main

import (
    //"fmt"
    "log"
    "net/http"

    "github.com/gorilla/websocket"
)

// Define the upgrader
var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        return true // Allow all connections by default
    },
}

// Handle WebSocket connections
func handleConnections(w http.ResponseWriter, r *http.Request) {
    // Upgrade initial GET request to a WebSocket
    ws, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Fatalf("Failed to upgrade connection: %v", err)
        return
    }
    defer ws.Close()

    // Send "Hello, world!" message to the client
    message := "Hello, world!\n"
    err = ws.WriteMessage(websocket.TextMessage, []byte(message))
    if err != nil {
        log.Printf("Failed to write message: %v", err)
        return
    }

    //fmt.Printf("Sent: %s", message)
}

func main() {
    // Create an HTTP server and handle WebSocket connections
    http.HandleFunc("/ws", handleConnections)
    log.Println("WebSocket server started on :8081")
    err := http.ListenAndServe(":8081", nil)
    if err != nil {
        log.Fatalf("Failed to start server: %v", err)
    }
}
