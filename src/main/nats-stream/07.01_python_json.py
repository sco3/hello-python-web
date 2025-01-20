#!/usr/bin/env -S uv run

import nats
import asyncio
import json
import time
import argparse
from nats.aio.client import Client as NATS
from typing import Dict, Any

STRING_FIELD: str = "string_field"
NUMBER_FIELD: str = "number_field"
INTEGER_FIELD: str = "integer_field"
NUMBER_LENGTH: int = 10  # Length of number_field (adjustable)
INTEGER_LENGTH: int = 10  # Length of integer_field (adjustable)

JSON_OVERHEAD: int = (
    len(STRING_FIELD)
    + len(NUMBER_FIELD)
    + len(INTEGER_FIELD)
    + NUMBER_LENGTH
    + INTEGER_LENGTH
    + 24
)


# Function to generate a JSON message of a specific size with fixed-length values
def generate_message(size_in_bytes: int, message_number: int) -> str:
    # Define the fixed lengths for fields
    string_length = (
        size_in_bytes - JSON_OVERHEAD
    )  # Length of string_field (adjustable)

    # Create fields with fixed length
    string_field = f"Message-{message_number:05d}".ljust(string_length, "0")
    number_field = f"{float(message_number + 0.01)}".ljust(NUMBER_LENGTH, "0")
    integer_field = (f"{message_number}").ljust(INTEGER_LENGTH, "0")

    # Create the message dictionary
    message: Dict[str, str] = {
        STRING_FIELD: string_field,
        NUMBER_FIELD: number_field,
        INTEGER_FIELD: integer_field,
    }

    # Serialize to JSON
    message_json = json.dumps(message)
    print(message_json, len(message_json))

    return message_json


# Function to benchmark the NATS server by publishing and subscribing to messages
async def benchmark_nats(
    nats_url: str, subject: str, num_messages: int, message_size: int
) -> None:
    # Connect to the NATS server
    nc = await nats.connect(nats_url)
    print(f"Connected to NATS server at {nats_url}")

    # Define the callback to handle the received message
    async def message_handler(msg: nats.aio.client.Msg) -> None:
        try:
            # Deserialize the JSON message
            received_message: Dict[str, Any] = json.loads(msg.data.decode())
            # You can add additional checks to validate the received message here if needed
        except Exception as e:
            print(f"Error during deserialization: {e}")

    # Subscribe to the subject to receive the message
    await nc.subscribe(subject, cb=message_handler)

    # Record the start time
    start_time = time.time()

    # Publish messages to the NATS server
    for i in range(num_messages):
        # Generate the message with incremental values based on message index
        message_json = generate_message(
            message_size, i + 1
        )  # Message numbers start from 1
        await nc.publish(subject, message_json.encode("utf-8"))
        if (i + 1) % 100 == 0:
            print(f"Published {i + 1} messages...")

    # Wait for all messages to be processed
    await nc.flush()

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print the benchmark results
    print(
        f"\nBenchmark results for {num_messages} messages of size {message_size} bytes:"
    )
    print(f"Total time taken: {elapsed_time:.4f} seconds")
    print(
        f"Messages per second: {num_messages / elapsed_time:.2f} messages/sec"
    )
    print(f"Message size: {len(message_json.encode('utf-8'))} bytes")

    # Close the NATS connection
    await nc.close()


# Main function to parse arguments and run the benchmark
def main() -> None:
    parser = argparse.ArgumentParser(
        description="NATS Benchmark Tool with Fixed-Length JSON Serialization/Deserialization"
    )
    parser.add_argument(
        "--nats_url",
        help="URL of the NATS server (e.g., nats://localhost:4222)",
    )
    parser.add_argument(
        "--subject", help="NATS subject to publish/subscribe to"
    )
    parser.add_argument(
        "--num_messages", type=int, help="Number of messages to publish"
    )
    parser.add_argument(
        "--message_size",
        type=int,
        help="Message size in bytes (target message size)",
    )

    args = parser.parse_args()

    # Run the benchmark
    asyncio.run(
        benchmark_nats(
            args.nats_url, args.subject, args.num_messages, args.message_size
        )
    )


if __name__ == "__main__":
    main()
