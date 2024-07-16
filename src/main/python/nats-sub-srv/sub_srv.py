#!/usr/bin/env -S poetry run python 
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def message_handler(msg):
    subject = msg.subject
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")
    
    # Extract the UUID from the subject
    if subject.startswith("test.in."):
        uuid = subject[len("test.in."):]
        response_subject = f"test.out.{uuid}"
        print (f"pubish hw  to {response_subject}")
        await nc.publish(response_subject, b'hello world')
        print(f"Published 'hello world' to '{response_subject}'")

async def run():
    global nc
    nc = NATS()

    print ('connect')
    try:
        await nc.connect("nats://localhost:4222", user='sys', password='pass')
    except ErrNoServers as e:
        print(f"Error: {e}")
        return

    print ('after connect')
    # Subscribe to the wildcard topic
    await nc.subscribe("test.in.*", cb=message_handler)

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
        
        print (time.time_ns())
    except (ErrConnectionClosed, KeyboardInterrupt):
        print("Connection closed")
    finally:
        await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
