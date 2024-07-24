package sco3;

import static java.lang.Thread.sleep;
import static java.lang.ThreadLocal.withInitial;
import static java.util.concurrent.Executors.newFixedThreadPool;
import static reactor.core.publisher.Mono.fromFuture;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicBoolean;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
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

	public long call(ThreadLocal<Connection> tnc) throws Exception {
		long start = System.currentTimeMillis();
		int n = 1000;
		ArrayList<Integer> result = new ArrayList<>(n);
		final AtomicBoolean run = new AtomicBoolean(true);
		final Connection nc = tnc.get();

		Flux<Integer> flux = Flux.range(1, n) //
				.map(i -> toBytes(i)) //
				.flatMap(bytes -> fromFuture(nc.request(SQUARE, bytes)))//
				.map(m -> fromMessage(m))//
				.doOnComplete(() -> run.set(false));

		flux.subscribe(i -> result.add(i));
		while (run.get()) {
			Thread.sleep(1);
		}
		System.out.println(result);

		long finish = System.currentTimeMillis();
		return finish - start;
	}

	private void runManyTimes() throws Exception {
		long start = System.currentTimeMillis();

		int poolSize = 100;
		ConcurrentLinkedQueue<Connection> conns = new ConcurrentLinkedQueue<>();

		ThreadPoolExecutor svc = (ThreadPoolExecutor) newFixedThreadPool(poolSize);
		ThreadLocal<Connection> nc = withInitial(//
				() -> {
					try {
						Connection c = Nats.connect("nats://localhost:4222");
						conns.add(c);
						return c;
					} catch (IOException | InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
						return null;
					}
				}//
		);

		int tests = 1000;
		for (int i = 0; i < tests; i++) {
			svc.execute(new Runnable() {
				@Override
				public void run() {
					try {
						call(nc);
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
			});
		}
		while (svc.getCompletedTaskCount() < tests) {
			sleep(1);
		}
		long finish = System.currentTimeMillis();
		long duration = finish - start;
		System.out.println("Time -> " + duration + " ms avg: " + ((double) duration) / tests);
		svc.shutdown();
		for (Connection c : conns) {
			c.close();
		}
	}

	public static void main(String[] args) throws Exception {
		NatsSquareClientReactor client = new NatsSquareClientReactor();
		client.runManyTimes();
	}

}
