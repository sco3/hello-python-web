#!/usr/bin/env -S poetry run python

import asyncio
import time
from nats.aio.client import Client as nats_client
from nats_common import NatsCommon


async def send_requests(client, subject, duration, num_requests):
    total_bytes_sent = 0
    total_bytes_received = 0
    rtt_times = []
    request_count = 0
    end_time = time.time() + duration

    async def handle_response(msg):
        nonlocal total_bytes_received, request_count
        request_end_time = time.time()
        rtt = request_end_time - msg.timestamp
        rtt_times.append(rtt)
        response_data = msg.data
        response_bytes = len(response_data)
        total_bytes_received += response_bytes
        request_count += 1

    # Subscribe to the subject
    await client.subscribe(subject, cb=handle_response)

    while time.time() < end_time:
        request_start_time = time.time()
        await client.publish(subject, b"Hello, world!\n", reply="response")
        request_end_time = time.time()

        # Track sent bytes
        total_bytes_sent += len(b"Hello, world!\n")

        await asyncio.sleep(0.01)  # Small delay to simulate real-world usage

    # Calculate average RTT
    if rtt_times:
        average_rtt = sum(rtt_times) / len(rtt_times)
    else:
        average_rtt = 0

    # Calculate throughput
    elapsed_time = duration
    total_bytes = total_bytes_sent + total_bytes_received
    if elapsed_time > 0:
        throughput_mb_per_s = (total_bytes / (1024 * 1024)) / elapsed_time
    else:
        throughput_mb_per_s = 0

    return {
        "request_count": request_count,
        "total_bytes_sent": total_bytes_sent,
        "total_bytes_received": total_bytes_received,
        "throughput_mb_per_s": throughput_mb_per_s,
        "average_rtt": average_rtt,
    }


async def benchmark(
    nats_servers, subject, num_clients, num_requests_per_client, duration
):
    clients = []
    for _ in range(num_clients):
        nc = nats_client()
        await NatsCommon.connect(nc)
        clients.append(nc)

    async def worker(client):
        return await send_requests(
            client, subject, duration, num_requests_per_client
        )

    # Create tasks
    tasks = [worker(client) for client in clients]
    results = await asyncio.gather(*tasks)

    # Aggregate results
    total_requests = sum(r["request_count"] for r in results)
    total_bytes_sent = sum(r["total_bytes_sent"] for r in results)
    total_bytes_received = sum(r["total_bytes_received"] for r in results)
    avg_rtt = sum(r["average_rtt"] for r in results) / len(results)
    throughput_mb_per_s = sum(r["throughput_mb_per_s"] for r in results) / len(
        results
    )

    # Close clients
    for client in clients:
        await client.close()

    print(f"Total requests: {total_requests}")
    print(f"Total bytes sent: {total_bytes_sent} bytes")
    print(f"Total bytes received: {total_bytes_received} bytes")
    print(f"Send + Receive throughput: {throughput_mb_per_s:.2f} MB/s")
    print(f"Average RTT: {avg_rtt:.4f} seconds")


if __name__ == "__main__":
    # NATS server URLs
    nats_servers = ["nats://localhost:4222"]

    # NATS subject for request-response
    subject = "benchmark.subject"

    # Number of clients and requests per client
    num_clients = 200
    num_requests_per_client = 1

    # Duration to run each client in seconds
    duration = 10

    # Run the benchmark
    asyncio.run(
        benchmark(
            nats_servers,
            subject,
            num_clients,
            num_requests_per_client,
            duration,
        )
    )
