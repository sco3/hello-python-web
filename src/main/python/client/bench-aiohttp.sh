#!/usr/bin/env -S poetry run python


import aiohttp
import asyncio
import time

async def send_requests(session, url, duration):
    data = "Hello, world!\n"
    data_bytes = len(data.encode('utf-8'))

    total_bytes_sent = 0
    total_bytes_received = 0
    rtt_times = []
    request_count = 0
    end_time = time.time() + duration

    while time.time() < end_time:
        request_start_time = time.time()

        try:
            async with session.post(url, data=data) as response:
                request_end_time = time.time()

                rtt = request_end_time - request_start_time
                rtt_times.append(rtt)

                response_data = await response.read()
                response_bytes = len(response_data)

                total_bytes_sent += data_bytes
                total_bytes_received += response_bytes
                request_count += 1
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")

    if rtt_times:
        average_rtt = sum(rtt_times) / len(rtt_times)
    else:
        average_rtt = 0

    elapsed_time = duration
    total_bytes = total_bytes_sent + total_bytes_received
    if elapsed_time > 0:
        throughput_mb_per_s = (total_bytes / (1024 * 1024)) / elapsed_time
    else:
        throughput_mb_per_s = 0

    return {
        'request_count': request_count,
        'total_bytes_sent': total_bytes_sent,
        'total_bytes_received': total_bytes_received,
        'throughput_mb_per_s': throughput_mb_per_s,
        'average_rtt': average_rtt
    }

async def benchmark(url, num_tasks, duration):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in range(num_tasks):
            task = asyncio.create_task(send_requests(session, url, duration))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
    
    # Aggregate results
    total_requests = sum(r['request_count'] for r in results)
    total_bytes_sent = sum(r['total_bytes_sent'] for r in results)
    total_bytes_received = sum(r['total_bytes_received'] for r in results)
    avg_rtt = sum(r['average_rtt'] for r in results) / len(results)
    throughput_mb_per_s = sum(r['throughput_mb_per_s'] for r in results) / len(results)

    print(f"Total requests: {total_requests}")
    print(f"Total bytes sent: {total_bytes_sent} bytes")
    print(f"Total bytes received: {total_bytes_received} bytes")
    print(f"Send + Receive throughput: {throughput_mb_per_s:.2f} MB/s")
    print(f"Average RTT: {avg_rtt:.4f} seconds")

if __name__ == "__main__":
    # URL of the HTTP server (without /echo)
    url = "http://localhost:8000"

    # Number of concurrent tasks and duration
    num_tasks = 2
    duration = 10

    # Run the benchmark
    asyncio.run(benchmark(url, num_tasks, duration))
