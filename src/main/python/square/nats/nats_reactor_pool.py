from asyncio import Queue
import asyncio
from nats_reactor import NatsReactor
import time

pool_size = 8  #
q = Queue(pool_size)


async def aggregate_task():
    r = await q.get()
    result = await r.aggregate(1000)
    await q.put(r)
    return result


async def check_execution(tasks):
    while True:
        done = True
        running = 0
        states = {}
        for task in tasks:
            state = task._state
            cnt = states.get(state, 0)
            states[state] = cnt + 1
            if not task.done():
                done = False

        print(states)
        if done:
            break
        await asyncio.sleep(1)


# while any(not task.done() for task in tasks):


async def benchmark():
    start = time.time()
    for i in range(pool_size):
        r = NatsReactor()
        await r.connect_nats()
        q.put_nowait(r)

    tasks = []
    for i in range(1000):
        tasks.append(asyncio.create_task(aggregate_task()))

    # await check_execution(tasks)

    result_list = await asyncio.gather(*tasks)

    dur = 1000 * (time.time() - start)
    result_sizes = set()
    for result in result_list:
        result_sizes.add(len(result))
    print(
        "took:",
        dur,
        "ms",
        "results:",
        len(result_list),
        "sizes:",
        result_sizes,
        "ms",
    )


if __name__ == "__main__":
    asyncio.run(benchmark())
