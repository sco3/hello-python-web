#!/usr/bin/env -S poetry run python
import asyncio
import websockets
import sys
import time
import concurrent.futures
import uvloop
import uuid

from nats.aio.client import Client as NATS

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HELLO = "Hello, world!\n"
HELLO_LEN = len(HELLO)


async def main():
    start = time.time_ns()
    id = 1  # uuid.uuid4()
    nc = NATS()
    resp_subj = f"test.in.{id}"
    req_subj = f"test.in.{id}"

    ready = asyncio.Event()
    try:
        await nc.connect("nats://localhost:4222", user="sys", password="pass")
    except ErrNoServers as e:
        print(f"Error: {e}")
        return

    async def receive(msg):
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")
        ready.set()

    await nc.subscribe(resp_subj, cb=receive)
    call_start = time.time_ns()
    await nc.publish(req_subj, b"hello world")
    await ready.wait()
    duration = (time.time_ns() - start) / 1_000_000
    call_duration = (time.time_ns() - call_start) / 1_000_000
    print(f"Full RTT: {duration} Call RTT: {call_duration}ms")


if __name__ == "__main__":
    asyncio.run(main())
