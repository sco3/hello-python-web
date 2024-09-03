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
from nats.errors import TimeoutError
from nats.js.api import (
    RetentionPolicy,
    StreamConfig,
    ConsumerConfig,
    DeliverPolicy,
    AckPolicy,
    PubAck,
)
from nats.js.client import JetStreamContext

from nats_common import NatsCommon


CONSUMER_NAME: str = "cons_lim1"
SUBJECT: str = "subj_lim"
STREAM: str = "stream_lim"


async def call(
    subscription,
) -> None:
    start: int = time.time_ns()

    # Pull a batch of messages from the consumer
    batch_size = 20
    try:
        msgs = await subscription.fetch(batch_size, timeout=2)

        # Process the messages
        for msg in msgs:
            data = msg.data

            async with NatsCommon.lock:
                NatsCommon.traffic += len(data)

            # print(f"Received message: {data.decode()}")
            await msg.ack()

    except TimeoutError as e:
        print("Timeout.")

    call_start = time.time_ns()

    duration = (time.time_ns() - start) / 1_000_000
    call_duration = (time.time_ns() - call_start) / 1_000_000

    async with NatsCommon.lock:
        NatsCommon.calls += len(msgs)
        NatsCommon.duration += duration
        NatsCommon.call_duration += call_duration


async def round(subsription) -> None:
    start: int = time.time_ns()
    end: int = start + 10 * 1_000_000_000  # 10 seconds

    while time.time_ns() < end:
        await call(subsription)

    duration = (time.time_ns() - start) / 1_000_000_000

    mb = NatsCommon.traffic / 1024 / 1024
    calls_sec = NatsCommon.calls / duration
    print(
        f"Calls: {NatsCommon.calls} in {duration} s {calls_sec} calls/s "
        "\n"
        f"Bytes: {NatsCommon.traffic} bytes "
        "\n"
        f"Throughput: {mb/duration} mb/s "
        "\n"
        f"Avg Full RTT: {NatsCommon.duration/NatsCommon.calls} ms "
        f"Avg Call RTT: {NatsCommon.call_duration/NatsCommon.calls} ms "
    )


async def async_main() -> None:
    NatsCommon.reset_stats()
    nc: NatsClient = NatsClient()
    await NatsCommon.connect(nc)
    js: JetStreamContext = nc.jetstream()
    consumer_config = ConsumerConfig(
        durable_name=CONSUMER_NAME,
        max_deliver=1,
        ack_policy=AckPolicy.EXPLICIT,
    )
    subscription = await js.pull_subscribe(
        SUBJECT,
        CONSUMER_NAME,
        STREAM,
        consumer_config,
    )

    await round(subscription)
    await nc.close()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
