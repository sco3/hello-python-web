from asyncio import Queue
import asyncio
from nats_reactor import NatsReactor
import time

pool_size = 2
q = Queue(pool_size)


async def aggregate_task():
    r = await q.get()
    result = await r.aggregate(1000)
    await q.put(r)
    return result


async def benchmark():
    start = time.time()
    for i in range(pool_size):
        r = NatsReactor()
        await r.connect_nats()
        q.put_nowait(r)

    tasks = []
    for i in range(2):
        tasks.append(asyncio.create_task(aggregate_task()))

#    while any(not task.done() for task in tasks):
#        print(q.qsize())
#        asyncio.sleep(0.1)

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
