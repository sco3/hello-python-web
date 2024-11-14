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


import gc
import sys
from collections import defaultdict


# Define a set of generic types to exclude from the analysis
EXCLUDED_TYPES = {} # {dict, list, tuple, set, type, frozenset}

def analyze_memory_usage():
    gc.collect()  # Clean up any unreferenced objects first
    memory_usage = defaultdict(int)  # Dictionary to hold memory usage grouped by object type
    
    total_size = 0
    # Iterate through all objects tracked by the garbage collector
    for obj in gc.get_objects():
        total_size += sys.getsizeof(obj)
        obj_type = type(obj)  # Get the type of the object

        # Only consider the object if it's not in the excluded types
        if obj_type not in EXCLUDED_TYPES:
            obj_size = sys.getsizeof(obj)  # Get the size of the object
            memory_usage[obj_type] += obj_size  # Aggregate memory usage by type

    # Create a sorted list of (object_type, total_size) tuples, sorted by total_size in descending order
    sorted_memory_usage = sorted(memory_usage.items(), key=lambda item: item[1], reverse=True)

    # Display top ten aggregated memory usage in MB
    total_size_mb = total_size / (1024 * 1024)  # 1 MB = 1024 * 1024 bytes
    print(f"Total Memory Size Used by All Objects: {total_size_mb:.2f} MB")

    print("Top 10 Memory-Consuming Object Types (excluding common types):")
    for obj_type, total_size in sorted_memory_usage[:10]:
        print(f"{obj_type.__name__}: {total_size / (1024 * 1024):.2f} MB")  # Convert size to MB
        


# Monitoring function for memory usage
def monitor_memory():
    process = psutil.Process()
    while True:
        mem_info = process.memory_info()
        rss_memory = mem_info.rss / (1024 * 1024)  # Convert bytes to MB
        print(f"{datetime.now(timezone.utc)} Memory Usage (RSS): {rss_memory:.2f} MB")
        analyze_memory_usage()
        time.sleep(10*60)  # Check memory every 10 minutes

if __name__ == "__main__":
    port = 8081
    ip = "0.0.0.0"
    print(f"Start ws server on ws://{ip}:{port}{PATH}")
    
    # Start the memory monitoring thread
    monitoring_thread = threading.Thread(target=monitor_memory, daemon=True)
    monitoring_thread.start()

    # Run the WebSocket server
    uvicorn.run(app, host=ip, port=port, log_level="critical" ) # , ws_per_message_deflate=False)
