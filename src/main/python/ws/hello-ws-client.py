import asyncio
import websockets
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# Configuration
SERVER_URI = "ws://localhost:8081"
CONNECTIONS_PER_THREAD = 100
THREAD_COUNT = 2
DURATION = 10  # seconds

async def websocket_client():
    start_time = time.time()
    async with websockets.connect(SERVER_URI) as websocket:
        while time.time() - start_time < DURATION:
            send_time = time.time()
            await websocket.send("Benchmark Message")
            response = await websocket.recv()
            rtt = time.time() - send_time
            # Process RTT and response for metrics
            print(f"RTT: {rtt:.4f} seconds, Response: {response}")

def run_websocket_clients():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [websocket_client() for _ in range(CONNECTIONS_PER_THREAD)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

def main():
    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        executor.map(lambda _: run_websocket_clients(), range(THREAD_COUNT))

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join(DURATION + 5)  # Extra time to ensure cleanup