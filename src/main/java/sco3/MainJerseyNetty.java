package sco3;

import static java.lang.System.getProperty;
import static java.lang.System.out;

import java.net.URI;

import org.glassfish.jersey.netty.httpserver.NettyHttpContainerProvider;
import org.glassfish.jersey.server.ResourceConfig;

import jakarta.ws.rs.core.UriBuilder;

public class MainJerseyNetty {

	public static void main(String[] args) {
		out.println("" //
				+ getProperty("java.vendor.version") //
		);

		URI baseUri = UriBuilder.fromUri("http://localhost/").port(8000).build();
		ResourceConfig resourceConfig = new ResourceConfig(HelloWorldResource.class);
		NettyHttpContainerProvider.createServer(baseUri, resourceConfig, false);
	}

}
