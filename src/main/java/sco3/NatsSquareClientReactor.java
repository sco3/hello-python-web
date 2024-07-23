package sco3;

import static reactor.core.publisher.Mono.fromFuture;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicBoolean;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
import reactor.core.Disposable;
import reactor.core.publisher.Flux;

public class NatsSquareClientReactor implements NatsSquare {

	byte[] toBytes(int i) {
		ByteBuffer buffer = ByteBuffer.allocate(ILEN);
		byte[] bytes = new byte[ILEN];
		buffer.putInt(0, i);
		buffer.get(0, bytes, 0, ILEN);
		return bytes;
	}

	int toInt(byte[] bytes) {
		ByteBuffer buffer = ByteBuffer.allocate(ILEN);
		buffer.put(0, bytes, 0, ILEN);
		return buffer.getInt(0);
	}

	int fromMessage(final Message m) {
		return toInt(m.getData());
	}

	public long run(Connection nc) throws Exception {
		long start = System.currentTimeMillis();
		int n = 1000;
		ArrayList<Integer> result = new ArrayList<>(n);
		final AtomicBoolean run = new AtomicBoolean(true);

		Flux<Integer> flux = Flux.range(1, n) //
				.map(i -> toBytes(i)) //
				.flatMap(bytes -> fromFuture(nc.request(SQUARE, bytes)))//
				.map(m -> fromMessage(m))//
				.doOnComplete(() -> run.set(false));

		flux.subscribe(i -> result.add(i));
		while (run.get()) {
			Thread.sleep(1);
		}

		long finish = System.currentTimeMillis();
		return finish - start;
	}

	private void runManyTimes(Connection nc) throws IOException, InterruptedException, Exception {
		long dur = 0;
		int tests = 1000;
		for (int i = 0; i < tests; i++) {
			dur += run(nc);
		}
		nc.close();
		System.out.println("Time -> " + dur + " ms avg: " + ((double) dur) / tests);
	}

	public static void main(String[] args) throws Exception {
		Connection nc = Nats.connect("nats://localhost:4222");
		NatsSquareClientReactor client = new NatsSquareClientReactor();
		client.runManyTimes(nc);
		nc.close();
	}

}
