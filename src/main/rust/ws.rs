use warp::Filter;
use futures_util::{StreamExt, SinkExt};

#[tokio::main]
async fn main() {
    // WebSocket route
    let websocket_route = warp::path("ws")
        .and(warp::ws())
        .map(|ws: warp::ws::Ws| {
            ws.on_upgrade(handle_socket)
        });

    // Start the server
    let port = 8081;
    println!("websocket start on {}", port);
    warp::serve(websocket_route)
        .run(([0, 0, 0, 0], port))
        .await;
}

async fn handle_socket(ws: warp::ws::WebSocket) {
    //println!("WebSocket connection established");
    let (mut tx, mut rx) = ws.split();

    while let Some(result) = rx.next().await {
        match result {
            Ok(msg) => {
                //println!("Received message: {:?}", msg);
                if !msg.is_close() {
                    //println!("send");
                    if tx.send(warp::ws::Message::text("Hello, world!\n")).await.is_err() {
                        eprintln!("websocket send error");
                    }
                }
            }
            Err(e) => {
                eprintln!("websocket error: {:?}", e);
                return;
            }
        }
    }
    //println!("WebSocket connection closed");
}