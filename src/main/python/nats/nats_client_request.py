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

import websockets

from nats_common import NatsCommon


async def call(anc: Union[NatsClient, None] = None) -> None:
    start: int = time.time_ns()

    if anc:
        nc: NatsClient = anc
    else:
        nc: NatsClient = NatsClient()

    if anc or await NatsCommon.connect(nc):
        id = uuid.uuid4()
        request_subject = NatsCommon.REQ_SUBJECT.format(id)
        call_start = time.time_ns()
        result = await nc.request(request_subject, NatsCommon.HELLO)
        duration = (time.time_ns() - start) / 1_000_000
        call_duration = (time.time_ns() - call_start) / 1_000_000

        async with NatsCommon.lock:
            NatsCommon.calls += 1
            NatsCommon.traffic += NatsCommon.HELLO_LEN
            NatsCommon.duration += duration
            NatsCommon.call_duration += call_duration
    if not anc:
        await nc.close()


async def round(anc: Union[NatsClient, None] = None) -> None:
    start: int = time.time_ns()
    end: int = start + 10 * 1_000_000_000  # 10 seconds

    while time.time_ns() < end:
        await call(anc)

    duration = (time.time_ns() - start) / 1_000_000_000

    mb = NatsCommon.traffic / 1024 / 1024
    expected = 2 * NatsCommon.calls * NatsCommon.HELLO_LEN
    calls_sec = NatsCommon.calls / duration
    print(
        f"Calls: {NatsCommon.calls} in {duration} s {calls_sec} calls/s "
        "\n"
        f"Bytes: {NatsCommon.traffic} / {expected} bytes "
        "\n"
        f"Throughput: {mb/duration} mb/s "
        "\n"
        f"Avg Full RTT: {NatsCommon.duration/NatsCommon.calls} ms "
        f"Avg Call RTT: {NatsCommon.call_duration/NatsCommon.calls} ms "
    )


async def two_rounds() -> None:
    print("\n" "First round with separate connections" "\n")
    await round()

    print("\n" "Second round with single connection" "\n")

    NatsCommon.reset_stats()
    nc: NatsClient = NatsClient()
    await NatsCommon.connect(nc)
    await round(nc)
    await nc.close()


def main() -> None:
    asyncio.run(two_rounds())


def prof():
    profiler = cProfile.Profile()
    profiler.enable()
    print("Nats client")
    main()
    profiler.disable()

    s = io.StringIO()

    # Create a Stats object and print the profiling results to the buffer
    sortby = "cumulative"
    ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    ps.print_stats()

    # Print the profiling results
    print(s.getvalue())


if __name__ == "__main__":
    main()
