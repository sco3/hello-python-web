#!/usr/bin/env -S uv run



import asyncio
import time
from nats.aio.client import Client as NATS

SUBJ="limi_subj"

async def publisher(nc, subject, message, num_messages):
    for _ in range(num_messages):
        await nc.publish(subject, message.encode())
    await nc.flush()

async def subscriber(nc, subject, num_messages, completed_event):
    received_count = 0

    async def message_handler(msg):
        nonlocal received_count
        received_count += 1
        if received_count >= num_messages:
            completed_event.set()

    await nc.subscribe(subject, cb=message_handler)

async def benchmark(message_size, num_messages):
    nc = NATS()
    await nc.connect("nats://localhost:4222")

    subject = SUBJ
    message = "x" * message_size
    completed_event = asyncio.Event()

    print(f"Starting benchmark: message_size={message_size}, num_messages={num_messages}")

    # Start subscriber
    subscriber_task = asyncio.create_task(subscriber(nc, subject, num_messages, completed_event))

    # Wait briefly to ensure the subscriber is ready
    await asyncio.sleep(1)

    # Start publisher
    start_time = time.time()
    await publisher(nc, subject, message, num_messages)

    # Wait for all messages to be received
    await completed_event.wait()
    end_time = time.time()

    elapsed_time = end_time - start_time
    throughput = num_messages / elapsed_time

    print(f"Benchmark completed: elapsed_time={elapsed_time:.2f}s, throughput={throughput:.2f} msgs/sec")

    await nc.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NATS Benchmark Script")
    parser.add_argument("--message_size", type=int, required=True, help="Size of each message in bytes")
    parser.add_argument("--num_messages", type=int, required=True, help="Number of messages to send and receive")

    args = parser.parse_args()

    asyncio.run(benchmark(args.message_size, args.num_messages))
