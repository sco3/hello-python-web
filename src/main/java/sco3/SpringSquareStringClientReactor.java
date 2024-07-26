package sco3;

import static java.lang.Thread.sleep;
import static java.lang.ThreadLocal.withInitial;
import static java.util.concurrent.Executors.newFixedThreadPool;
import static reactor.core.publisher.Mono.fromFuture;

import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicLong;

import org.glassfish.grizzly.utils.Charsets;
import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

public class SpringSquareStringClientReactor implements NatsSquare {
	AtomicLong mCount = new AtomicLong(0);

	String toStr(int i) {
		return Integer.toString(i);
	}

	int toInt(String s) {
		return Integer.parseInt(s);
	}

	int req(int i) {
		// WebClient client = WebClient.create("http://localhost:800");

		// Mono<String> response =
		// client.get().uri("/square").retrieve().bodyToMono(String.class);

		// response.subscribe(System.out::println);
		return 0;

	}

	public long call() throws Exception {
//		long start = System.currentTimeMillis();
//		int n = 1000;
//		ArrayList<Integer> result = new ArrayList<>(n);
//		final AtomicBoolean run = new AtomicBoolean(true);
//
//		Flux<Integer> flux = (Flux.range(1, n) //
//				.map(this::toStr) //
//				.flatMap(bytes -> fromFuture(nc.request(SQUARE, bytes)))//
//				.map(this::fromMessage)//
//				.doOnComplete(() -> run.set(false))//
//				.subscribeOn(Schedulers.single()) //
//		);
//
//		flux.subscribe(i -> result.add(i));
//		while (run.get()) {
//			Thread.sleep(1);
//		}
//		// System.out.println(result);
//
//		long finish = System.currentTimeMillis();
//		return finish - start;
		return 0;
	}

	private void runManyTimes() throws Exception {
		long start = System.currentTimeMillis();
		int tests = 1000;
		int poolSize = 100;

		ThreadPoolExecutor svc = (ThreadPoolExecutor) newFixedThreadPool(poolSize);

		for (int i = 0; i < tests; i++) {
			svc.execute(new Runnable() {
				@Override
				public void run() {
					try {
						call();
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
	}

	public static void main(String[] args) throws Exception {
		SpringSquareStringClientReactor client = new SpringSquareStringClientReactor();
		client.runManyTimes();
	}

}
