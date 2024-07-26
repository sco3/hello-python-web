package sco3;

import static java.lang.Thread.sleep;
import static java.lang.ThreadLocal.withInitial;
import static java.util.concurrent.Executors.newFixedThreadPool;
import static reactor.core.publisher.Mono.fromFuture;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;

public class NatsSquareClientReactor implements NatsSquare {
	AtomicLong mCount = new AtomicLong(0);
	ThreadLocal<ByteBuffer> mBuffer = new ThreadLocal<>() {
		@Override
		protected ByteBuffer initialValue() {
			long cnt = mCount.incrementAndGet();
			System.out.println(cnt + " " + Thread.currentThread());
			return ByteBuffer.allocate(ILEN);
		}
	}; // ().withInitial(() -> ByteBuffer.allocate(ILEN));

	byte[] toBytes(int i) {
		ByteBuffer buffer = mBuffer.get();
		var bytes = new byte[ILEN];
		buffer.putInt(0, i);
		buffer.get(0, bytes, 0, ILEN);
		return bytes;
	}

	int toInt(byte[] bytes) {
		ByteBuffer buffer = mBuffer.get();
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

		Flux<Integer> flux = (Flux.range(1, n) //
				.map(this::toBytes) //
				.flatMap(bytes -> fromFuture(extracted(nc, bytes)))//
				.map(this::fromMessage)//
				.doOnComplete(() -> run.set(false))//
				.subscribeOn(Schedulers.single()) //
		);

		flux.subscribe(i -> result.add(i));
		while (run.get()) {
			Thread.sleep(1);
		}
		// System.out.println(result);

		long finish = System.currentTimeMillis();
		return finish - start;
	}

	private CompletableFuture<Message> extracted(final Connection nc, byte[] bytes) {
		return nc.request(SQUARE, bytes);
	}

	private void runManyTimes() throws Exception {
		long start = System.currentTimeMillis();
		int tests = 1000;
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
