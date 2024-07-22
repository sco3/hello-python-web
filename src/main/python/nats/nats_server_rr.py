#!/usr/bin/env -S poetry run python3

import asyncio
import time
from nats.aio.client import Client as NATS
from nats_common import NatsCommon


async def main():
    nc = NATS()
    if await NatsCommon.connect(nc):

        async def message_handler(msg):
            # print(f"Received message: {msg.subject} {msg.data.decode()} Send {NatsCommon.HELLO} to {msg.reply}")
            await msg.respond(NatsCommon.HELLO)

        await nc.subscribe(NatsCommon.REQ_ALL, cb=message_handler)

        await asyncio.Event().wait()


if __name__ == "__main__":

    asyncio.run(main())
