package sco3;

import static reactor.core.publisher.Mono.just;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import reactor.core.publisher.Mono;

@RestController
public class SringSquareStringController {

	@GetMapping("/square/{number}")
	public Mono<String> getSquare(@PathVariable int number) {
		number = number * number;
		return just(Integer.toString(number));
	}

}
