package sco3;

import static java.lang.Integer.parseInt;
import static java.lang.System.out;
import static org.glassfish.grizzly.utils.Charsets.ASCII_CHARSET;

import io.nats.client.Connection;
import io.nats.client.Dispatcher;
import io.nats.client.Nats;
import io.nats.client.Options;

public class NatsSquareStringService implements NatsSquare {

	public static void main(String[] args) throws Exception {
		Options options = new Options.Builder().server(SERVER).userInfo(USER, PASS).build();

		Connection nc = Nats.connect(options);

		Dispatcher d = nc.createDispatcher((msg) -> {
			int in = parseInt(new String(msg.getData(), ASCII_CHARSET));
			System.out.println("Received:" + in);

			int out = in * in;
			nc.publish(msg.getReplyTo(), Integer.toString(out).getBytes());
		});
		out.println("Subscribe to subject: " + SQUARE);
		d.subscribe(SQUARE);
	}

}
