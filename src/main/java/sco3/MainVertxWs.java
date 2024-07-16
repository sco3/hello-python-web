package sco3;

import static java.lang.System.out;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Vertx;
import io.vertx.core.http.ServerWebSocket;
import io.vertx.core.http.HttpServer;

public class MainVertxWs extends AbstractVerticle {

	@Override
	public void start() {
		HttpServer server = vertx.createHttpServer();

		int port = 8081;
		server.webSocketHandler(webSocket -> {
			// Handle incoming WebSocket connection
			handleWebSocketConnection(webSocket);
		}).listen(port, result -> {
			if (result.succeeded()) {
				out.println("WebSocket server is listening on port " + port);
			} else {
				out.println("Failed to start WebSocket server: " + result.cause());
			}
		});
	}

	private void handleWebSocketConnection(ServerWebSocket webSocket) {
		// When a message is received
		webSocket.textMessageHandler(message -> {
			out.println("Received message: " + message);
			webSocket.writeTextMessage("Hello, World!");
		});

		// When the connection is closed
		webSocket.closeHandler(v -> {
			out.println("WebSocket connection closed");
		});
	}

	public static void main(String[] args) {
		Vertx vertx = Vertx.vertx();
		vertx.deployVerticle(new MainVertxWs());
	}
}
