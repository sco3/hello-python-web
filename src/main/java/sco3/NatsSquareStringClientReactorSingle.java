package sco3;

import static reactor.core.publisher.Mono.fromFuture;

import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

import org.glassfish.grizzly.utils.Charsets;

import io.nats.client.Connection;
import io.nats.client.Message;
import io.nats.client.Nats;
import io.nats.client.Options;
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;

public class NatsSquareStringClientReactorSingle implements NatsSquare {
	AtomicLong mCount = new AtomicLong(0);

	byte[] toBytes(int i) {
		return Integer.toString(i).getBytes(Charsets.ASCII_CHARSET);
	}

	int toInt(byte[] bytes) {
		return Integer.parseInt(new String(bytes, Charsets.ASCII_CHARSET));
	}

	int fromMessage(final Message m) {
		return toInt(m.getData());
	}

	public long call(Connection nc) throws Exception {
		long start = System.currentTimeMillis();
		int results = 1000;
		ArrayList<Integer> result = new ArrayList<>(results);
		final AtomicBoolean run = new AtomicBoolean(true);

		Flux<Integer> flux = (Flux.range(1, results) //
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

		long finish = System.currentTimeMillis();
		return finish - start;
	}

	public static void main(String[] args) throws Exception {
		Options options = (new Options.Builder()//
				.server(SERVER)//
				.userInfo(USER, PASS)//
				.build() //
		);
		Connection nc = Nats.connect(options);

		NatsSquareStringClientReactorSingle client = ( //
		new NatsSquareStringClientReactorSingle() //
		);
		long duration = client.call(nc);
		System.out.println("Took: " + duration + " ms");
		nc.close();
	}
}
