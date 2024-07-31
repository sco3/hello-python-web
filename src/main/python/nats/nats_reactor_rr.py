import asyncio
from typing import Union

from nats.aio.client import Client as NatsClient
from nats.aio.client import Msg
from observable import Observable
from rx import operators as ops
import rx
import uuid
import traceback

from nats_common import NatsCommon


async def call(nc: NatsClient, data: bytes) -> bytes:
    subject = NatsCommon.SQUARE_SUBJECT
    print("Request to: ", subject)
    result: Msg = await nc.request(subject, data)
    out: bytes = result.data
    print(out)
    return out


def call_as_future(nc: NatsClient, data: bytes) -> Observable:
    loop = asyncio.get_event_loop()
    future = loop.create_task(call(nc, data))
    return rx.from_future(future)


def to_bytes(i: int) -> bytes:
    return str(i).encode()


def from_message(m) -> bytes:
    return 0


async def main() -> None:
    nc: NatsClient = NatsClient()
    NatsCommon.setClusterNodes(1)
    await NatsCommon.connect(nc)

    #    r = await call(nc, b"2")
    #    print(f"{r}")

    n: int = 1
    observable: Observable = rx.range(1, n + 1).pipe(
        ops.map(to_bytes),
        ops.flat_map(lambda data: call_as_future(nc, data)),
    )
    observable.subscribe(
        on_next=lambda i: print(f"Received: {i}"),
        on_error=lambda e: print(f"Error: {e}\n{traceback.format_exc()}"),
        on_completed=lambda: print("Finish."),
    )

    await asyncio.sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
