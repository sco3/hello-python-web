from asyncio import Queue
import asyncio
from nats_reactor import NatsReactor
import time

pool_size = 1
q = Queue(pool_size)
result_list = []


async def benchmark():
    start = time.time()
    for i in range(pool_size):
        r = NatsReactor()
        await r.connect_nats()
        q.put_nowait(r)

    for i in range(1000):
        r = await q.get()
        result_list.append(await r.aggregate(1000))
        r = await q.put(r)

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
