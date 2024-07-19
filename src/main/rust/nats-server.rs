//use bytes::Bytes;
use async_nats::ConnectOptions;
use futures::StreamExt;
#[tokio::main]
async fn main() -> Result<(), async_nats::Error> {
    println!("start");
    // set user and password
    let conn_opts = ConnectOptions::new() //
        .user_and_password("sys".to_string(), "pass".to_string());

    // Connect to the NATS server

    let client = async_nats::connect_with_options("localhost:4222", conn_opts).await?;

    // Subscribe to the "messages" subject
    let mut subscriber = client.subscribe("req.*").await?;

    // Receive and process messages
    while let Some(message) = subscriber.next().await {
        //println!("Received message {:?}", message);
        if let Some(subj) = message.reply {
            //println!("reply subj: {}", subj);
            client.publish(subj, "Hello, world!\n".into()).await?;
        }
    }

    println!("done");

    Ok(())
}
