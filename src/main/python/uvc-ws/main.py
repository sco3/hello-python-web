#!/usr/bin/env -S poetry run python

from fastapi import FastAPI, WebSocket
import uvicorn
import logging
import time
import asyncio
import uvloop

import psutil
import threading

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


logging.basicConfig(level=logging.CRITICAL)

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    # print(f"Received message: {time.time_ns()} {data}")
    await websocket.send_text("Hello, world!\n")
    await websocket.close()


# Monitoring function
def monitor_memory():
    process = psutil.Process()
    while True:
        mem_info = process.memory_info()
        rss_memory = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
        print(f"Memory Usage (RSS): {rss_memory:.2f} MB")
        time.sleep(5)  # Interval for checking memory (every 5 seconds)


if __name__ == "__main__":
    # Start the memory monitoring thread
    monitoring_thread = threading.Thread(target=monitor_memory, daemon=True)
    monitoring_thread.start()

    # Run the WebSocket server
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="critical")
