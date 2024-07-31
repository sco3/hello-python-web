from asyncio import Event
import asyncio
import time
import traceback
from typing import Union
import uuid

from nats.aio.client import Client as NatsClient
from nats.aio.client import Msg
from observable import Observable
from rx import operators as ops
import rx

from nats_common import NatsCommon


async def call(nc: NatsClient, data: bytes) -> bytes:
    subject = NatsCommon.SQUARE_SUBJECT
    result: Msg = await nc.request(subject, data)
    return result.data


def call_as_future(nc: NatsClient, data: bytes) -> Observable:
    loop = asyncio.get_event_loop()
    future = loop.create_task(call(nc, data))
    return rx.from_future(future)


def to_bytes(i: int) -> bytes:
    return str(i).encode()


def from_bytes(m: bytes) -> int:
    return int(m.decode())


async def main() -> None:
    start: int = time.time_ns()
    finish: Event = Event()

    nc: NatsClient = NatsClient()
    NatsCommon.setClusterNodes(1)
    await NatsCommon.connect(nc)

    #    r = await call(nc, b"2")
    #    print(f"{r}")

    n: int = 100000
    observable: Observable = rx.range(1, n + 1).pipe(
        ops.map(to_bytes),
        ops.flat_map(lambda data: call_as_future(nc, data)),
        ops.map(from_bytes),
    )
    result: list = []
    observable.subscribe(
        on_next=lambda i: result.append(i),
        on_error=lambda e: print(f"Error: {e}\n{traceback.format_exc()}"),
        on_completed=lambda: finish.set(),
    )

    await finish.wait()
    duration_ms: int = (time.time_ns() - start) / 1000_1000

    print(f"Took: {duration_ms} {result}")


if __name__ == "__main__":
    asyncio.run(main())
