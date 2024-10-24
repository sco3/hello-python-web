#!/usr/bin/env -S poetry run python3

from asyncio import Event
import asyncio
import time
import traceback
from typing import List

from nats.aio.client import Client as NatsClient
from nats.aio.client import Msg

from nats_common import NatsCommon


class NatsCaller:
    def __init__(self, servers: int = 1):
        self.nc: NatsClient = NatsClient()
        self.servers: int = servers

    async def connect_nats(self) -> None:
        """Connects to the NATS server."""
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
        result: List[int] = []
        for i in range(1000):
            r = await self.call(self.to_bytes(i + 1))
            result.append(self.from_bytes(r))
        return result


async def main():
    start: int = time.time_ns()
    manager = NatsCaller()
    await manager.connect_nats()
    await manager.aggregate()
    duration_ms: float = (time.time_ns() - start) / 1_000_000
    print(f"Took: {duration_ms} ms calls:{NatsCommon.calls}")


if __name__ == "__main__":
    asyncio.run(main())
