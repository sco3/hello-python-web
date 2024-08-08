#!/usr/bin/env -S poetry run python3

from asyncio import Event
from asyncio import Task
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

    @staticmethod
    def from_message(msg: Msg) -> int:
        """
        Convert bytes back to an integer.

        :param msg: The message to convert.
        :return: The integer representation of the bytes.
        """

        return int(msg.data.decode())

    async def aggregate(self, n: int = 1000) -> List[int]:
        """
        Perform the main logic for making requests and processing results.

        :param n: The number of requests to process.
        :return: A list of results.
        """
        finish: Event = Event()
        observable: ObsObs = rx.range(1, n + 1).pipe(
            ops.map(self.to_bytes),
            ops.flat_map(
                lambda data: rx.from_future(
                    asyncio.get_event_loop().create_task(
                        self.nc.request(NatsCommon.SQUARE_SUBJECT, data)
                    )
                )
            ),
            ops.map(self.from_message),
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
