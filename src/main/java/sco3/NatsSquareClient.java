package sco3;

import java.nio.ByteBuffer;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;

public class NatsSquareClient implements NatsSquare {
	ByteBuffer buffer = ByteBuffer.allocate(ILEN);
	byte[] bytes = new byte[ILEN];

	int square(//
			Connection nc, int i //
	) throws InterruptedException, ExecutionException {
		buffer.putInt(0, i);
		buffer.get(0, bytes, 0, ILEN);
		CompletableFuture<Message> res = nc.request(SQUARE, bytes);
		byte[] outBytes = res.get().getData();
		buffer.put(0, outBytes, 0, ILEN);
		return buffer.getInt(0);
	}

	public void run(Connection nc) throws Exception {
		long start = System.currentTimeMillis();
		var n = 1000;
		for (int i = 0; i < n; i++) {
			var i2 = square(nc, i + 1);
			System.out.println(i2);
		}
		long finish = System.currentTimeMillis();
		System.out.println("Time: " + (finish - start) + " ms");
	}

	public static void main(String[] args) throws Exception {
		NatsSquareClient client = new NatsSquareClient();
		Connection nc = Nats.connect("nats://localhost:4222");
		client.run(nc);
		nc.close();
	}

}
