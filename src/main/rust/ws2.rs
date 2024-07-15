use ws2::{Pod, WebSocket};
use log2::info;

struct Worker;

impl ws2::Handler for Worker {
    fn on_open(&mut self, _ws: &WebSocket) -> Pod {
        Ok(())
    }

    fn on_close(&mut self, _ws: &WebSocket) -> Pod {
        Ok(())
    }

    fn on_message(&mut self, ws: &WebSocket, _msg: String) -> Pod {
        let n = ws.send("Hello, world!\n");
        Ok(n?)
    }
}

fn main() -> Pod {
    let _log2 = log2::start();
    let address = "127.0.0.1:8081";
    let mut worker = Worker {};

    info!("listen on: {address}");
    let mut server = ws2::listen(address)?;

    loop {
        let _ = server.process(&mut worker, 0.5);
        // do other stuff
    }
}
