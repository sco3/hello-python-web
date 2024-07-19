#!/usr/bin/env -S poetry run python

import requests
import time


def benchmark(url, duration):
    # Data to send
    data = "Hello, world!\n"
    data_bytes = len(data.encode("utf-8"))

    # Initialize variables to track throughput, RTT, and request count
    total_bytes_sent = 0
    total_bytes_received = 0
    rtt_times = []
    request_count = 0
    start_time = time.time()

    while time.time() - start_time < duration:
        request_start_time = time.time()

        # Send POST request and get the response
        response = requests.post(url, data=data)

        request_end_time = time.time()

        # Ensure the request was successful
        if response.status_code == 200:
            rtt = request_end_time - request_start_time
            rtt_times.append(rtt)

            response_data = response.content
            response_bytes = len(response_data)

            total_bytes_sent += data_bytes
            total_bytes_received += response_bytes
            request_count += 1

    # Calculate average RTT
    if rtt_times:
        average_rtt = sum(rtt_times) / len(rtt_times)
    else:
        average_rtt = 0

    # Calculate throughput
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        total_bytes = total_bytes_sent + total_bytes_received
        throughput_mb_per_s = (total_bytes / (1024 * 1024)) / elapsed_time
    else:
        throughput_mb_per_s = 0

    # Print results
    print(f"Total requests: {request_count}")
    print(f"Total bytes sent: {total_bytes_sent} bytes")
    print(f"Total bytes received: {total_bytes_received} bytes")
    print(f"Send + Receive throughput: {throughput_mb_per_s:.2f} MB/s")
    print(f"Average RTT: {average_rtt:.4f} seconds")


if __name__ == "__main__":
    # URL of the HTTP server (without /echo)
    url = "http://localhost:8000"

    # Duration to run the benchmark in seconds
    duration = 10

    # Run the benchmark
    benchmark(url, duration)
