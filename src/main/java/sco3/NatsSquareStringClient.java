package sco3;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
import io.nats.client.Options;

public class NatsSquareStringClient implements NatsSquare {

	int square(//
			Connection nc, int i //
	) throws InterruptedException, ExecutionException {
		byte[] bytes = Integer.toString(i).getBytes();
		CompletableFuture<Message> res = nc.request(SQUARE, bytes);
		Message message = res.get();
		byte[] outBytes = message.getData();
		int out = Integer.parseInt(new String(outBytes));
		return out;
	}

	public void run(Connection nc) throws Exception {
		long start = System.currentTimeMillis();
		int n = 1000;
		for (int i = 0; i < n; i++) {
			// int out =
			square(nc, i + 1);
			// System.out.println(out);
		}
		long finish = System.currentTimeMillis();
		System.out.println("Time: " + (finish - start) + " ms");
	}

	public static void main(String[] args) throws Exception {
		NatsSquareStringClient client = new NatsSquareStringClient();
		Options options = (new Options.Builder()//
				.server(SERVER)//
				.userInfo(USER, PASS)//
				.build() //
		);

		Connection nc = Nats.connect(options);
		client.run(nc);
		nc.close();
	}

}
