


from fastapi import FastAPI, WebSocket
import threading
import psutil
from datetime import datetime, timezone
import time

# Monitoring function for memory usage
def monitor_memory():
    process = psutil.Process()
    while True:
        mem_info = process.memory_info()
        rss_memory = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
        print(f"{datetime.now(timezone.utc)} Memory Usage (RSS): {rss_memory:.2f} MB")
        #analyze_memory_usage()
        time.sleep(10)  # Check memory every 10 seconds


app = FastAPI()
PATH = "/ws"

@app.websocket(PATH)
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    #print("Client connected")
    try:
        while True:
            # Wait for any message from the client or a disconnect signal
            message = await websocket.receive()

            # Check if the client has closed the connection
            if message["type"] == "websocket.disconnect":
                #print("Client disconnected gracefully")
                break

            # Process the received text message if still connected
            if "text" in message:
                data = message["text"]
                #print(f"Received message: {data}")

                response = f"Hello world!"
                await websocket.send_text(response)

            await asyncio.sleep(0.0001)  # Small sleep to prevent flooding
    except Exception as e:
        #print(f"Connection closed with exception: {e}")
        pass
    finally:
        await websocket.close()



# Start the memory monitoring thread
monitoring_thread = threading.Thread(target=monitor_memory, daemon=True)
monitoring_thread.start()
