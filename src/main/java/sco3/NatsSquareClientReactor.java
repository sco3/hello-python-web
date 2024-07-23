package sco3;

import static reactor.core.publisher.Flux.range;
import static reactor.core.publisher.Mono.fromFuture;

import java.nio.ByteBuffer;

import io.nats.client.Connection;
import io.nats.client.Nats;
import reactor.core.publisher.Flux;

public class NatsSquareClientReactor implements NatsSquare {
	ByteBuffer buffer = ByteBuffer.allocate(ILEN);
	byte[] bytes = new byte[ILEN];

	byte[] toBytes(int i) {
		buffer.putInt(0, i);
		buffer.get(0, bytes, 0, ILEN);
		return bytes;
	}

	int toInt(byte[] bytes) {
		buffer.put(0, bytes, 0, ILEN);
		return buffer.getInt(0);
	}

	public void run(Connection nc) throws Exception {
		long start = System.currentTimeMillis();
		Flux flux = range(1, 1000)//
				.map(i -> toBytes(i))//
				.map(bts -> fromFuture(nc.request(SQUARE, bts))//
						.map(b -> toInt(b.getData()))//
				);
		
		long finish = System.currentTimeMillis();
		System.out.println("Time -> " + (finish - start) + " ms");
	}

	public static void main(String[] args) throws Exception {
		NatsSquareClient client = new NatsSquareClient();
		Connection nc = Nats.connect("nats://localhost:4222");
		client.run(nc);
		nc.close();
	}

}
