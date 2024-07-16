#!/usr/bin/env -S poetry run python
import asyncio
import websockets
import time
import concurrent.futures
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


total = 0
total_lock = asyncio.Lock()


async def ping_pong():
    async with websockets.connect("ws://localhost:8081/ws") as websocket:
        await websocket.send("Hello, world!\n")
        response = await websocket.recv()
        # print (f"{response}")


async def client():
    global total
    global total_lock
    tasks = set()
    round_trips = 0
    start = time.time_ns()
    max_tasks = 200
    timeok = True

    while timeok or (len(tasks) > 0):
        timeok = time.time_ns() - start < 10_000_000_000
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
    task1 = asyncio.create_task(client())
    task2 = asyncio.create_task(client())
    await asyncio.gather(task1, task2)


asyncio.run(main())
print("Total:", total)
