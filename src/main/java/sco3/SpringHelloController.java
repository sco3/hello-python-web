package sco3;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SpringHelloController {

	@GetMapping("/")
	public String getHello() {
		return "Hello, World!\n";
	}

}
