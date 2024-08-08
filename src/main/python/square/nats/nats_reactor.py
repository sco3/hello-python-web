#!/usr/bin/env -S poetry run python3

from asyncio import Event
import asyncio
import time
import traceback
from typing import List, ClassVar

from nats.aio.client import Client as NatsClient
from nats.aio.client import Msg
from rx import operators as ops
import rx
from rx.core.observable.observable import Observable as ObsObs
from rx.core.typing import Observable

from nats_common import NatsCommon


class NatsReactor:
    number: ClassVar[int] = 1000
    tests: ClassVar[int] = 1000

    def __init__(self, servers: int = 1):
        self.nc: NatsClient = NatsClient()
        self.servers: int = servers

    async def connect_nats(self) -> None:
        """Connects to the NATS server."""
        if not self.nc.is_connected:
            NatsCommon.setClusterNodes(self.servers)
            await NatsCommon.connect(self.nc)

    async def call(self, data: bytes) -> bytes:
        """
        Send a call to the NATS server and return the response data.

        :param data: The data to send to the NATS server.
        :return: The response data from the NATS server.
        """
        result: Msg = await self.nc.request(NatsCommon.SQUARE_SUBJECT, data)
        NatsCommon.calls += 1
        return result.data

    def call_as_future(self, data: bytes) -> Observable:
        """
        Wrap the call in an asyncio task and return an Observable.

        :param data: The data to send to the NATS server.
        :return: An Observable wrapping the asyncio task.
        """
        loop = asyncio.get_event_loop()
        future = loop.create_task(self.call(data))
        return rx.from_future(future)

    @staticmethod
    def to_bytes(i: int) -> bytes:
        """
        Convert an integer to bytes.

        :param i: The integer to convert.
        :return: The bytes representation of the integer.
        """
        return str(i).encode()

    @staticmethod
    def from_bytes(data: bytes) -> int:
        """
        Convert bytes back to an integer.

        :param data: The bytes to convert.
        :return: The integer representation of the bytes.
        """
        return int(data.decode())

    async def aggregate(self, n: int = 1000) -> List[int]:
        """
        Perform the main logic for making requests and processing results.

        :param n: The number of requests to process.
        :return: A list of results.
        """
        finish: Event = Event()
        observable: ObsObs = rx.range(1, n + 1).pipe(
            ops.map(self.to_bytes),
            ops.flat_map(lambda data: self.call_as_future(data)),
            ops.map(self.from_bytes),
        )
        result: List[int] = []
        observable.subscribe(
            on_next=lambda i: result.append(i),
            on_error=lambda e: print(f"Error: {e}\n{traceback.format_exc()}"),
            on_completed=lambda: finish.set(),
        )

        await finish.wait()
        return result


async def main() -> None:
    start: int = time.time_ns()
    manager = NatsReactor()
    await manager.connect_nats()
    for i in range(NatsReactor.tests):
        await manager.aggregate(NatsReactor.number)
        
    duration_ms: float = (time.time_ns() - start) / 1_000_000
    print(f"Took: {duration_ms} ms calls:{NatsCommon.calls}")


if __name__ == "__main__":
    asyncio.run(main())
