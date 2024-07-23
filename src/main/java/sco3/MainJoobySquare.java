package sco3;

import static java.lang.System.getProperty;
import static java.lang.System.out;

import java.util.function.Supplier;

import io.jooby.Jooby;
import io.jooby.MediaType;
import io.jooby.ServerOptions;
import io.jooby.rxjava3.Reactivex;
import io.reactivex.rxjava3.core.Single;

public class MainJoobySquare extends Jooby {

	{
		use(Reactivex.rx());

		ServerOptions opts = new ServerOptions().setPort(7576);
		opts.setWorkerThreads(200);
		setServerOptions(opts);

		get("/api/square/unary/old/{number}", ctx -> {
			int number = ctx.path("number").intValue();
			return number * number;
		});

		get("/api/square/unary/{number}", ctx -> {
			ctx.setResponseType(MediaType.json);
			int number = ctx.path("number").intValue();
			return Single //
					.fromCallable(() -> number * number) //
					.map(it -> it);
		});
	}

	public static void main(String[] args) {
		Supplier<Jooby> provider = MainJoobySquare::new;
		out.println("" //
				+ getProperty("java.vendor.version") //
				+ " " + provider.getClass().getSimpleName() //
		);

		runApp(args, provider);
	}
}