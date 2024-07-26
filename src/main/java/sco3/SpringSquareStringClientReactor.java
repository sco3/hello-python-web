package sco3;

import static java.lang.String.format;
import static java.lang.System.out;
import static java.lang.Thread.sleep;
import static java.util.concurrent.Executors.newFixedThreadPool;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpClient.Version;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.reactive.function.client.WebClient;

import reactor.core.publisher.Mono;

public class SpringSquareStringClientReactor implements NatsSquare {
	static int mTests = 1000;
	static int mCalls = 1000;
	AtomicLong mCount = new AtomicLong(0);
	private int mPoolSize = 100;

	String toStr(int i) {
		return Integer.toString(i);
	}

	int toInt(String s) {
		return Integer.parseInt(s);
	}

	void reqBuildin( //
			final int[] result, //
			List<CompletableFuture<Void>> futures//
	) throws Exception {
		for (int call = 0; call < mCalls; call++) {
			HttpClient client = (HttpClient.newBuilder()//
					.version(Version.HTTP_2) //
					.build()//
			);

			String url = format("http://localhost:8000/square/%d", call + 1);
			HttpRequest req = (HttpRequest.newBuilder()//
					.uri(URI.create(url))//
					.GET()//
					.build()//
			);

			CompletableFuture<HttpResponse<String>> response = client.sendAsync(req,
					HttpResponse.BodyHandlers.ofString());

			CompletableFuture<String> s = response.thenApplyAsync(HttpResponse::body);
			final int n = call;
			futures.add(s.thenAcceptAsync(body -> result[n] = toInt(body)));
		}
	}

	int req(int i) {
		WebClient client = WebClient.create("http://localhost:800");

		Mono<String> response = client.get().uri("/square").retrieve().bodyToMono(String.class);

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

	private static void printResults(int n, int[][] results) {
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < mCalls; j++) {
				out.print(results[i][j] + " ");
			}
			out.println();
		}
	}

	public static void main(String[] args) throws Exception {
		SpringSquareStringClientReactor cli = new SpringSquareStringClientReactor();
		long start = System.currentTimeMillis();
		int n = 10;
		int[][] results = new int[n][mCalls];
		List<CompletableFuture<Void>> futureResults = new ArrayList<>();

		for (int i = 0; i < n; i++) {
			results[i] = new int[mCalls];
			cli.reqBuildin(results[i], futureResults);
		}
		CompletableFuture.allOf(futureResults.toArray(new CompletableFuture<?>[0]));
		long duration = System.currentTimeMillis() - start;
		out.println("Time -> " + duration + " ms");
		printResults(n, results);

	}

}
