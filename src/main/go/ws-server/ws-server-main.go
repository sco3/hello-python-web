package main

import (
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

    // Read messages from the client
    for {
        _, msg, err := ws.ReadMessage()
        if err != nil {
            // Check if the error is a normal closure
            if websocket.IsCloseError(err, websocket.CloseNormalClosure) {
                // Skip logging for normal closure
                return // Exit the loop gracefully
            }
            log.Printf("Error reading message: %v", err)
            return // Exit the loop for other errors
        }

        // Optionally echo the message back to the client
        err = ws.WriteMessage(websocket.TextMessage, msg)
        if err != nil {
            log.Printf("Error sending message: %v", err)
            return
        }
    }
}

func main() {
    // Create an HTTP server and handle WebSocket connections
    http.HandleFunc("/ws", handleConnections)
    port := ":8082"
    log.Println("WebSocket server started on ", port)
    err := http.ListenAndServe(port, nil)
    if err != nil {
        log.Fatalf("Failed to start server: %v", err)
    }
}
