#!/usr/bin/env -S poetry run python3

import asyncio
import time

from nats.aio.client import Client as NATS

from nats_common import NatsCommon


async def main():
    nc = NATS()
    if await NatsCommon.connect(nc):

        async def message_handler(msg):
            # print(f"Received message: {msg.subject} {msg.data.decode()}")
            subject = msg.subject
            uuid = subject[NatsCommon.REQ_PREFIX_LEN :]
            res_sub = NatsCommon.RES_SUBJECT.format(uuid)
            # print(f"Send {NatsCommon.HELLO_STR} to {res_sub}")
            await msg.respond(NatsCommon.HELLO)

        await nc.subscribe(NatsCommon.REQ_ALL, cb=message_handler)
        await nc.flush()

        await asyncio.Event().wait()


#        while True:
#            await asyncio.sleep(1)


if __name__ == "__main__":

    asyncio.run(main())
