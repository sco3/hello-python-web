package sco3;

import static java.lang.System.getProperty;
import static java.lang.System.out;

import io.vertx.core.AbstractVerticle;
import io.vertx.core.Vertx;

public class MainVertx extends AbstractVerticle {

	@Override
	public void start() {
		vertx.createHttpServer().requestHandler(req -> {
			req //
					.response() //
					.putHeader("content-type", "text/plain") //
					.end("Hello, World!\n"); //
		}).listen(8000);
	}

	public static void main(String[] args) {
		out.println("" //
				+ getProperty("java.vendor.version") //
				+ " " //
				+ MainVertx.class.getSimpleName() //
		);

		Vertx vertx = Vertx.vertx();
		vertx.deployVerticle(new MainVertx());
	}
}