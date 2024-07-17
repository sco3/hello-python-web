#!/usr/bin/env -S poetry run python
import asyncio
import websockets
import sys
import time
import concurrent.futures
import uvloop
import uuid
import nanoid
from nats_common import NatsCommon

from nats.aio.client import Client as NATS

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def main():
    start = time.time_ns()

    nc = NATS()

    if await NatsCommon.connect(nc):
        id = uuid.uuid4()

        ready = asyncio.Event()

        async def response(msg):
            subject = msg.subject
            data = msg.data.decode()
            # print(f"Received a message on '{subject}': {data}")
            ready.set()

        req_sub = NatsCommon.REQ_SUBJECT.format(id)
        res_sub = NatsCommon.RES_SUBJECT.format(id)

        await nc.subscribe(res_sub, cb=response)
        call_start = time.time_ns()
        await nc.publish(req_sub, NatsCommon.HELLO)
        await ready.wait()
        duration = (time.time_ns() - start) / 1_000_000
        call_duration = (time.time_ns() - call_start) / 1_000_000
        print(f"Full RTT: {duration} Call RTT: {call_duration}ms")


if __name__ == "__main__":
    asyncio.run(main())
