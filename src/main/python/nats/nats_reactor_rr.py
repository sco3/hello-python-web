import asyncio
from typing import Union

from nats.aio.client import Client as NatsClient
from observable import Observable
from rx import operators as ops
import rx

from nats_common import NatsCommon


async def call(nc: NatsClient) -> None:
    id: str = uuid.uuid4()
    request_subject = NatsCommon.REQ_SUBJECT.format(id)
    result = await nc.request(request_subject, NatsCommon.HELLO)


def to_bytes(i: int) -> bytes:
    return str(i).encode()


async def main() -> None:
    nc: NatsClient = NatsClient()
    NatsCommon.setClusterNodes(1)
    await NatsCommon.connect(nc)

    observable: Observable = rx.range(1, 11).pipe(ops.map(to_bytes))
    observable.subscribe(
        on_next=lambda i: print(f"Ok:{i}"),
        on_error=lambda e: print(f"Error: {e}"),
        on_completed=lambda: print("Finish."),
    )


if __name__ == "__main__":
    asyncio.run(main())
