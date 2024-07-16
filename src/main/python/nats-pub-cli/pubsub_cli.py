#!/usr/bin/env -S poetry run python
import asyncio
import websockets
import sys
import time
import concurrent.futures
import uvloop
import uuid

from nats.aio.client import Client as NATS

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HELLO = "Hello, world!\n"
HELLO_LEN = len(HELLO)

async def receive(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")

async def ping_pong():
    id=1 # uuid.uuid4()
    nc = NATS()
    resp_subj = f"test.resp.{id}"
    req_subj= f"test.req.{id}"

    print ('connect')
    try:
        await nc.connect("nats://localhost:4222", user='sys', password='pass')
    except ErrNoServers as e:
        print(f"Error: {e}")
        return
        
    print (f"sub {resp_subj}")
    await nc.subscribe(resp_subj, cb=receive)
    print (f"pub {req_subj}")
    await nc.publish(req_subj, b'hello world')
    await asyncio.sleep(10)


async def main():
    await ping_pong ()

if __name__ == '__main__':
    asyncio.run(main())
