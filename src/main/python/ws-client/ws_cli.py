#!/usr/bin/env -S poetry run python
import asyncio
import websockets
import sys
import time
import concurrent.futures
import uvloop
from _asyncio import Task

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


HELLO = "Hello, world!\n"
HELLO_LEN = len(HELLO)

total = 0
recv = 0
sent = 0
rtt = 0
min_rtt = sys.maxsize
max_rtt = 0
total_lock = asyncio.Lock()
port = "8081"


async def ping_pong():
    global recv
    global sent
    global rtt
    global min_rtt
    global max_rtt

    async with websockets.connect(f"ws://localhost:{port}/ws") as websocket:
        start = time.time_ns()
        if False:
            await websocket.send(HELLO)
            response = await websocket.recv()
        else:
            task = asyncio.create_task(websocket.recv())
            await websocket.send(HELLO)
            response = await task

        end = time.time_ns()
        async with total_lock:
            recv += len(response)
            sent += HELLO_LEN
            cur_rtt = end - start
            rtt += cur_rtt

            if cur_rtt > max_rtt:
                max_rtt = cur_rtt

            if cur_rtt < min_rtt:
                min_rtt = cur_rtt

        # print (response)


async def client(duration_ns: int):
    global total
    global total_lock
    tasks = set()
    round_trips = 0
    start = time.time_ns()
    max_tasks = 200
    timeok = True

    while timeok or (len(tasks) > 0):
        timeok = time.time_ns() - start < duration_ns
        tasks = {task for task in tasks if not task.done()}
        if timeok and (len(tasks) < 200):
            # print (cnt)
            task = asyncio.create_task(ping_pong())
            async with total_lock:
                total += 1
            tasks.add(task)
            # task.add_done_callback(tasks.discard)

        await asyncio.sleep(0.0001)


async def main():
    duration_ns = 10_000_000_000
    print(f"Duration: {duration_ns / 1_000_000_000} seconds port: {port}")

    await asyncio.gather(
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
        asyncio.create_task(client(duration_ns)),
    )
    print(
        "Total rounds:",
        total,
        "req/s:",
        total * 1_000_000_000 / duration_ns,
        "sent:",
        sent,
        "bytes recv:",
        recv,
        "bytes expected:",
        total * HELLO_LEN,
        "bytes \nAverage rtt:",
        rtt / total / 1000_000,
        "ms",
        "min rtt:",
        min_rtt / 1000_000,
        "ms",
        "max rtt:",
        max_rtt / 1000_000,
        "ms",
    )


asyncio.run(main())
