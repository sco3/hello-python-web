#!/usr/bin/env -S poetry run python3

import asyncio
import time
from nats.aio.client import Client as NATS
from nats_common import NatsCommon


async def main() -> None:
    nc: NATS = NATS()
    NatsCommon.setClusterNodes(1)
    if await NatsCommon.connect(nc):
        async def message_handler(msg) -> None:
            i: int = int(msg.data.decode())
            i = i * i
            await msg.respond(str(i).encode())

        await nc.subscribe(NatsCommon.SQUARE_SUBJECT, cb=message_handler)

        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
