package sco3;

import static reactor.core.publisher.Mono.fromFuture;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

import org.glassfish.grizzly.utils.Charsets;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
import io.nats.client.Options;
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;

public class NatsSquareStringClientReactorNoPool implements NatsSquare {
	AtomicLong mCount = new AtomicLong(0);
	private int mTests = 1000;
	private int mNumber = 1000;

	private ArrayList<List<Integer>> mResults = new ArrayList<>(mTests);

	byte[] toBytes(int i) {
		return Integer.toString(i).getBytes(Charsets.ASCII_CHARSET);
	}

	int toInt(byte[] bytes) {
		return Integer.parseInt(new String(bytes, Charsets.ASCII_CHARSET));
	}

	int fromMessage(final Message msg) {
		return toInt(msg.getData());
	}

	public long aggregate(Connection nc, int number) throws Exception {
		long start = System.currentTimeMillis();

		final AtomicBoolean run = new AtomicBoolean(true);
		List<Integer> result = new ArrayList<>(number);

		Flux<Integer> flux = (Flux.range(1, number) //
				.map(this::toBytes) //
				.flatMap(bytes -> fromFuture(nc.request(SQUARE, bytes)))//
				.map(this::fromMessage)//
				.doOnComplete(() -> run.set(false))//
				.subscribeOn(Schedulers.single()) //
		);

		flux.subscribe(i -> result.add(i));
		while (run.get()) {
			Thread.sleep(1);
		}
		mResults.add(result);
		long finish = System.currentTimeMillis();
		return finish - start;
	}

	private void runManyTimes() throws Exception {
		long start = System.currentTimeMillis();
		Options options = (new Options.Builder()//
				.server(SERVER)//
				.userInfo(USER, PASS)//
				.build() //
		);

		Connection c = Nats.connect(options);

		for (int i = 0; i < mTests; i++) {
			aggregate(c, mNumber);
		}
		long finish = System.currentTimeMillis();
		long duration = finish - start;
		Set<Integer> sizes = new HashSet<>();
		for (List<Integer> r : mResults) {
			sizes.add(r.size());
		}
		System.out.println("" //
				+ "Time -> " + duration //
				+ " ms avg: " + ((double) duration) / mTests //
				+ " tests: " + mResults.size() //
				+ " sizes: " + sizes //
		);
		c.close();
	}

	public static void main(String[] args) throws Exception {
		NatsSquareStringClientReactorNoPool client = new NatsSquareStringClientReactorNoPool();
		client.runManyTimes();
	}
}
