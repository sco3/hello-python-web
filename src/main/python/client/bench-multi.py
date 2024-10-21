#!/usr/bin/env -S poetry run python

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def worker(url, num_requests, duration):
    data = "Hello, world!\n"
    data_bytes = len(data.encode("utf-8"))

    total_bytes_sent = 0
    total_bytes_received = 0
    rtt_times = []
    request_count = 0
    end_time = time.time() + duration

    while time.time() < end_time:
        request_start_time = time.time()

        try:
            response = requests.post(
                url, data=data, timeout=5
            )  # Adding a timeout to prevent hangs
            response.raise_for_status()
            request_end_time = time.time()

            rtt = request_end_time - request_start_time
            rtt_times.append(rtt)

            response_data = response.content
            response_bytes = len(response_data)

            total_bytes_sent += data_bytes
            total_bytes_received += response_bytes
            request_count += 1
        except requests.RequestException as e:
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
        "request_count": request_count,
        "total_bytes_sent": total_bytes_sent,
        "total_bytes_received": total_bytes_received,
        "throughput_mb_per_s": throughput_mb_per_s,
        "average_rtt": average_rtt,
    }


def benchmark(url, num_threads, num_requests_per_thread, duration):
    results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(worker, url, num_requests_per_thread, duration)
            for _ in range(num_threads)
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Aggregate results
    total_requests = sum(r["request_count"] for r in results)
    total_bytes_sent = sum(r["total_bytes_sent"] for r in results)
    total_bytes_received = sum(r["total_bytes_received"] for r in results)
    avg_rtt = sum(r["average_rtt"] for r in results) / len(results)
    throughput_mb_per_s = sum(r["throughput_mb_per_s"] for r in results) / len(results)

    print(f"Total requests: {total_requests}")
    print(f"Total bytes sent: {total_bytes_sent} bytes")
    print(f"Total bytes received: {total_bytes_received} bytes")
    print(f"Send + Receive throughput: {throughput_mb_per_s:.2f} MB/s")
    print(f"Average RTT: {avg_rtt:.4f} seconds")


if __name__ == "__main__":
    # URL of the HTTP server (without /echo)
    url = "http://localhost:8000"

    # Number of threads and requests per thread
    num_threads = 2
    num_requests_per_thread = 200

    # Duration to run each thread in seconds
    duration = 10

    # Run the benchmark
    benchmark(url, num_threads, num_requests_per_thread, duration)
