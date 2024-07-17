#!/usr/bin/env -S poetry run python3

import asyncio
import time
import uvloop

from nats.aio.client import Client as NATS

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def message_handler(msg):
    print(f"Received message: {msg.subject} {msg.data.decode()}")
    subject = msg.subject
    if subject.startswith("test.in."):
        uuid = subject[len("test.in.") :]
        response_subject = f"test.out.{uuid}"
        print(f"pubish hw  to {response_subject}")
        await nc.publish(response_subject, b"hello world")
        print(f"Published 'hello world' to '{response_subject}'")


async def main():
    global nc
    nc = NATS()

    await nc.connect(
        servers=["nats://localhost:4222"], user="sys", password="pass"
    )
    await nc.subscribe("test.in.*", cb=message_handler)
    await nc.flush()
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Start")
    asyncio.run(main())
    print("Finish")
