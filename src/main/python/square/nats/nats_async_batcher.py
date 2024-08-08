#!/usr/bin/env -S poetry run python3

import asyncio
import time
from typing import List

from nats.aio.client import Client as NatsClient
from nats.aio.client import Msg

from nats_common import NatsCommon


class NatsBatcher:
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

    async def call(self, n: int) -> int:
        """
        Send a call to the NATS server and return the response data.

        :param data: The data to send to the NATS server.
        :return: The response data from the NATS server.
        """
        data = NatsBatcher.to_bytes(n)
        result: Msg = await self.nc.request(NatsCommon.SQUARE_SUBJECT, data)
        NatsCommon.calls += 1
        return NatsBatcher.from_bytes(result.data)

    async def aggregate(self, n: int = 1000) -> List[int]:
        """
        Perform the main logic for making requests and processing results.

        :param n: The number of requests to process.
        :return: A list of results.
        """
        result = []
        tasks = []

        for i in range(n):
            task = asyncio.create_task(self.call(i))
            tasks.append(task)

        result = await asyncio.gather(*tasks)

        return result


async def main() -> None:
    start: int = time.time_ns()
    manager = NatsBatcher()
    await manager.connect_nats()
    sizes = set()
    for i in range(1000):
        r = await manager.aggregate()
        sizes.add(len(r))

    duration_ms: float = (time.time_ns() - start) / 1_000_000
    print(f"Took: {duration_ms} ms calls:{NatsCommon.calls} sizes:{sizes}")


if __name__ == "__main__":
    asyncio.run(main())
