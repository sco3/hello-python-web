package sco3;

import static java.lang.System.out;

import io.vertx.core.Vertx;
import io.vertx.core.http.HttpClient;
import io.vertx.core.http.HttpClientOptions;
import io.vertx.core.http.WebSocket;
import io.vertx.core.http.WebSocketConnectOptions;

public class MainVertxWsClient {
	public static void main(String[] args) {
		Vertx vertx = Vertx.vertx();

		HttpClientOptions options = new HttpClientOptions() //
				.setSsl(false).setDefaultHost("localhost");
		HttpClient client = vertx.createHttpClient(options);

		WebSocketConnectOptions connectOptions = new WebSocketConnectOptions().setPort(8081).setHost("localhost")
				.setURI("/ws");

		client.webSocket(connectOptions, webSocketAsyncResult -> {
			if (webSocketAsyncResult.succeeded()) {
				WebSocket webSocket = webSocketAsyncResult.result();
				webSocket.textMessageHandler(message -> {
					out.println("Received message: " + message);
					webSocket.close();
					vertx.close();
				});
				webSocket.writeTextMessage("Hello, world!\n");
				webSocket.exceptionHandler(e -> {
					out.println(e.getMessage());
				});
			} else {
				webSocketAsyncResult.cause().printStackTrace();
			}
		});
	}
}
