package sco3;

import static java.lang.String.format;
import static java.lang.System.out;
import static java.lang.Thread.sleep;
import static java.util.concurrent.Executors.newFixedThreadPool;
import static reactor.core.publisher.Mono.fromFuture;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpClient.Version;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;

public class SpringSquareStringClientReactor implements NatsSquare {
	static int mTests = 1000;
	static int mCalls = 1000;
	AtomicLong mCount = new AtomicLong(0);
	private int mPoolSize = 100;

	CompletableFuture<String> getFuture(HttpClient client, String url) {
		HttpRequest req = (HttpRequest.newBuilder()//
				.uri(URI.create(url))//
				.GET()//
				.build()//
		);

		CompletableFuture<HttpResponse<String>> response = client//
				.sendAsync(req, HttpResponse.BodyHandlers.ofString());

		CompletableFuture<String> s = response//
				.thenApplyAsync(HttpResponse::body);
		return s;
	}

	int[] call() throws Exception {
		final AtomicBoolean run = new AtomicBoolean(true);
		final int[] result = new int[mCalls];
		final HttpClient client = (HttpClient.newBuilder()//
				.version(Version.HTTP_2) //
				.build()//
		);
		Flux<Integer> flux = Flux.range(1, mCalls)//
				.map(i -> format("http://127.0.0.1:8000/square/%d", i)) //
				.flatMap(url -> fromFuture(getFuture(client, url), false)) //
				.map(Integer::parseInt).doOnComplete(() -> run.set(false))//
				.subscribeOn(Schedulers.single()); //

		AtomicInteger idx = new AtomicInteger(0);
		flux.subscribe(i -> {
			result[idx.getAndAdd(1)] = i;
		});
		while (run.get()) {
			Thread.sleep(1);
		}
		return result;
	}

	private void runParallel() throws Exception {
		long start = System.currentTimeMillis();

		ThreadPoolExecutor svc = (ThreadPoolExecutor) newFixedThreadPool(mPoolSize);

		for (int i = 0; i < mTests; i++) {
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
		while (svc.getCompletedTaskCount() < mTests) {
			sleep(1);
		}
		long finish = System.currentTimeMillis();
		long duration = finish - start;
		System.out.println("Time -> " + duration + " ms avg: " + ((double) duration) / mTests);
		svc.shutdown();
	}

	public static void main(String[] args) throws Exception {
		SpringSquareStringClientReactor cli = new SpringSquareStringClientReactor();
		long start = System.currentTimeMillis();
		cli.runParallel();
		long duration = System.currentTimeMillis() - start;
		out.println("Time: " + duration + " ms runs: " + mTests + " avg: " + duration / mTests);

	}

}
