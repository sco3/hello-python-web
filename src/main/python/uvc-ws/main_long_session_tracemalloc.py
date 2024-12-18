#!/usr/bin/env -S poetry run python

from fastapi import FastAPI, WebSocket
import uvicorn
import logging
import time
from datetime import datetime, timezone
import asyncio
import psutil
import threading
import sys
import gc
import tracemalloc
from websockets.extensions.permessage_deflate import PerMessageDeflate
import zlib


# Set logging level
logging.basicConfig(level=logging.CRITICAL)

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

# Monitoring function for memory usage
def monitor_memory():
    process = psutil.Process()
    while True:
        mem_info = process.memory_info()
        rss_memory = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
        print(f"{datetime.now(timezone.utc)} Memory Usage (RSS): {rss_memory:.2f} MB")
        print("ws count:", sum(1 for obj in gc.get_objects() if isinstance(obj, WebSocket)))
        print("pmd count:", sum(1 for obj in gc.get_objects() if isinstance(obj, PerMessageDeflate)))
        #print("zC count:", sum(1 for obj in gc.get_objects() if isinstance(obj, zlib.compress)))
        snapshot = tracemalloc.take_snapshot()
        # Filter and display the top memory-consuming object types
        top_stats = snapshot.statistics("traceback")

        print("Top memory-consuming object types:")
        
        for index, stat in enumerate(top_stats[:10], 1):  # Show top 10
            print(f"{index}. {stat}")
            
        time.sleep(10)  # Check memory every 10 seconds

if __name__ == "__main__":
    tracemalloc.start()
    port = 8081
    ip = "0.0.0.0"
    print(f"Start ws server on ws://{ip}:{port}{PATH}")

    # Start the memory monitoring thread
    monitoring_thread = threading.Thread(target=monitor_memory, daemon=True)
    monitoring_thread.start()

    # Run the WebSocket server
    uvicorn.run(app, host=ip, port=port, log_level="critical", ws_per_message_deflate=False) #, ws="wsproto", limit_concurrency=10)
