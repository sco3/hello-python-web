package sco3;

import static java.lang.System.getProperty;
import static java.lang.System.out;

import java.net.URI;

import org.glassfish.jersey.grizzly2.httpserver.GrizzlyHttpServerFactory;
import org.glassfish.jersey.server.ResourceConfig;

import jakarta.ws.rs.core.UriBuilder;

public class MainJerseyGrizzly {
	public static void main(String[] args) {
		out.println("" //
				+ getProperty("java.vendor.version") //
		);

		URI baseUri = UriBuilder.fromUri("http://localhost/").port(8000).build();
		ResourceConfig resourceConfig = new ResourceConfig(JerseyResource.class);
		GrizzlyHttpServerFactory.createHttpServer(baseUri, resourceConfig);
	}

}
