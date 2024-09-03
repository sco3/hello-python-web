#!/usr/bin/env -S poetry run python

#
#
# async def subscribe_to_messages(self,
#                                component_type: str,
#                                callback: Callable[[str, bytes], Any]):
#    await logger.ainfo("consume_messages: subscribing to events on %s",
#                       NATS_URL)
#    self.heartbeat_task = asyncio.create_task(self.heartbeat(component_type))
#    consumer_cfg = ConsumerConfig(
#        durable_name=f"{self.consumer_name}_{component_type}",
#        deliver_policy=DeliverPolicy.ALL,
#        ack_policy=AckPolicy.EXPLICIT,
#        filter_subject=self.subject.format(component_type=component_type,
#                                           hostname=self.hostname),
#    )
#
#    await self.jet_stream.add_consumer(NATS_STREAM_NAME, consumer_cfg)
#    # Clear the stop event to ensure we can start the loop
#    self.stop_event.clear()
#
#    while not self.stop_event.is_set():
#        try:
#            subscription = await self.jet_stream.pull_subscribe(
#                self.subject.format(component_type=component_type,
#                                    hostname=self.hostname),
#                durable=f"{self.consumer_name}_{component_type}",
#                config=consumer_cfg
#            )
#            msgs: list[Msg] = await subscription.fetch(10, timeout=NATS_TIMEOUT)
#            await asyncio.gather(
#                *[self.process_message(msg, callback, component_type) for msg in
#                  msgs])
#        except nats.errors.TimeoutError as exc:
#            pass


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
from nats.js.client import JetStreamContext

from nats.js.api import (
    RetentionPolicy,
    StreamConfig,
    ConsumerConfig,
    DeliverPolicy,
    AckPolicy,
    PubAck,
)

CONSUMER_NAME: str = "cons_lim1"
SUBJECT: str = "subj_lim"
STREAM: str = "stream_lim"


async def call(
    js: JetStreamContext,
    consumer_config: ConsumerConfig,
) -> None:
    start: int = time.time_ns()

    messages = await js.pull_subscribe(
        SUBJECT,
        CONSUMER_NAME,
        STREAM,
        consumer_config,
    )

    # Pull a batch of messages from the consumer
    batch_size = 1
    msgs = await messages.fetch(batch_size, timeout=5)

    # Process the messages
    for msg in msgs:
        print(f"Received message: {msg.data.decode()}")
        await msg.ack()

    call_start = time.time_ns()

    duration = (time.time_ns() - start) / 1_000_000
    call_duration = (time.time_ns() - call_start) / 1_000_000

    async with NatsCommon.lock:
        NatsCommon.calls += 1
        NatsCommon.traffic += NatsCommon.HELLO_LEN
        NatsCommon.duration += duration
        NatsCommon.call_duration += call_duration


async def round(js: JetStreamContext, cons_conf) -> None:
    start: int = time.time_ns()
    end: int = start + 10 * 1_000_000_000  # 10 seconds

    while time.time_ns() < end:
        await call(js, cons_conf)

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

    await round(js, consumer_config)
    await nc.close()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
