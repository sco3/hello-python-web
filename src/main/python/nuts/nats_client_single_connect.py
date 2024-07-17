#!/usr/bin/env -S poetry run python
import asyncio
import cProfile
import concurrent.futures
import io
import pstats
import sys
import time
from typing import Union
import uuid

from nats.aio.client import Client as NatsClient
from pkg_resources._vendor.importlib_resources._common import Anchor
import uvloop
import websockets

from nats_common import NatsCommon


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def call(nc: NatsClient) -> None:
    start: int = time.time_ns()

    id = uuid.uuid4()

    ready = asyncio.Event()

    async def response(msg):
        subject = msg.subject
        async with NatsCommon.lock:
            NatsCommon.traffic += len(msg.data)

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

    async with NatsCommon.lock:
        NatsCommon.calls += 1
        NatsCommon.traffic += NatsCommon.HELLO_LEN
        NatsCommon.duration += duration
        NatsCommon.call_duration += call_duration


async def round(nc: NatsClient) -> None:
    start: int = time.time_ns()
    end: int = start + 10 * 1_000_000_000  # 10 seconds

    while time.time_ns() < end:
        await call(nc)

    duration = (time.time_ns() - start) / 1_000_000_000

    mb = NatsCommon.traffic / 1024 / 1024
    expected = 2 * NatsCommon.calls * NatsCommon.HELLO_LEN
    print(
        f"Calls: {NatsCommon.calls} in {duration} s"
        "\n"
        f"Bytes: {NatsCommon.traffic} / {expected} bytes "
        "\n"
        f"Throughput: {mb/duration} mb/s "
        "\n"
        f"Avg Full RTT: {NatsCommon.duration/NatsCommon.calls} "
        f"Avg Call RTT: {NatsCommon.call_duration/NatsCommon.calls} ms "
    )


async def main() -> None:
    nc: NatsClient = NatsClient()
    await NatsCommon.connect(nc)
    await round(nc)
    await nc.close()


if __name__ == "__main__":
    asyncio.run(main())
