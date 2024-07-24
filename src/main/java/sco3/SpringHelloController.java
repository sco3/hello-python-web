package sco3;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Mono;

@RestController
public class SpringHelloController {

	@GetMapping("/")
	public Mono<String> getHello() {
		return Mono.just("Hello, World!\n");
	}

}
