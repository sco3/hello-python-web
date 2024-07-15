package com.example;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Vertx;
import io.vertx.core.http.ServerWebSocket;
import io.vertx.core.http.HttpServer;

public class WebSocketServer extends AbstractVerticle {

    @Override
    public void start() {
        HttpServer server = vertx.createHttpServer();

        server.websocketHandler(webSocket -> {
            // Handle incoming WebSocket connection
            handleWebSocketConnection(webSocket);
        }).listen(8080, result -> {
            if (result.succeeded()) {
                System.out.println("WebSocket server is listening on port 8080");
            } else {
                System.out.println("Failed to start WebSocket server: " + result.cause());
            }
        });
    }

    private void handleWebSocketConnection(ServerWebSocket webSocket) {
        // When a message is received
        webSocket.textMessageHandler(message -> {
            System.out.println("Received message: " + message);
            webSocket.writeTextMessage("Hello, World!");
        });

        // When the connection is closed
        webSocket.closeHandler(v -> {
            System.out.println("WebSocket connection closed");
        });
    }

    public static void main(String[] args) {
        Vertx vertx = Vertx.vertx();
        vertx.deployVerticle(new WebSocketServer());
    }
}
