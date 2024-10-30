#!/usr/bin/env -S poetry run python

import asyncio
import websockets
import time
import statistics

# Global variables for statistics
total_requests_sent = 0
total_requests_received = 0
rtt_list = []

async def ping_pong(uri, duration_ns):
    global total_requests_sent, total_requests_received, rtt_list
    end_time = time.time_ns() + duration_ns

    async with websockets.connect(uri) as ws:
        while time.time_ns() < end_time:
            # Prepare ping message
            ping_time = time.time_ns()
            await ws.send("ping")  # Sending a ping message
            total_requests_sent += 1
            
            # Wait for any response
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=duration_ns / 1_000_000_000)  # Convert ns to seconds
                total_requests_received += 1
                # Calculate RTT
                rtt = time.time_ns() - ping_time
                rtt_list.append(rtt)
            except asyncio.TimeoutError:
                print("No response received, request timed out.")
            
            await asyncio.sleep(0.1)  # Small sleep to avoid flooding

async def run_tasks(n, duration_ns):
    uri = 'ws://localhost:8081/ws'  # WebSocket server URL
    tasks = [asyncio.create_task(ping_pong(uri, duration_ns)) for _ in range(n)]
    await asyncio.gather(*tasks)

def print_stats(start_time, duration_ns):
    global total_requests_sent, total_requests_received, rtt_list
    elapsed_time_sec = (time.time_ns() - start_time) / 1_000_000_000  # Convert ns to seconds
    sent_req_per_sec = total_requests_sent / elapsed_time_sec
    received_req_per_sec = total_requests_received / elapsed_time_sec

    print(f"Total Requests Sent: {total_requests_sent}")
    print(f"Total Requests Received: {total_requests_received}")
    print(f"Sent Requests per Second: {sent_req_per_sec:.2f} req/s")
    print(f"Received Requests per Second: {received_req_per_sec:.2f} req/s")
    if rtt_list:
        print(f"RTT - Average: {statistics.mean(rtt_list) / 1_000_000} ms")  # Convert ns to ms
        print(f"RTT - Min: {min(rtt_list) / 1_000_000} ms")  # Convert ns to ms
        print(f"RTT - Max: {max(rtt_list) / 1_000_000} ms")  # Convert ns to ms
    else:
        print("No RTT data collected.")

async def main():
    n = 100  # Number of tasks to create
    duration_ns = 10_000_000_000  # Duration of each task in nanoseconds
    uri = 'ws://localhost:8081/ws'  # WebSocket server URL

    # Print the expected duration and number of tasks
    print(f"Starting WebSocket test with {n} tasks.")
    print(f"Expected duration of the test: {duration_ns / 1_000_000_000} seconds")  # Convert ns to seconds
    print(f"WebSocket URL: {uri}")

    # Record the start time
    start_time = time.time_ns()

    await run_tasks(n, duration_ns)
    print_stats(start_time, duration_ns)

if __name__ == '__main__':
    asyncio.run(main())
