package sco3;

import io.jooby.Jooby;
import io.jooby.ServerOptions;

public class Main extends Jooby {

	{
		ServerOptions opts = new ServerOptions().setPort(8000);
		setServerOptions(opts);
		get("/", ctx -> "Hello, World!\n");
	}

	public static void main(String[] args) {
		runApp(args, Main::new);
	}
}