import asyncio
import os
from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing.managers import ValueProxy
from multiprocessing.managers import DictProxy
from nats_reactor import NatsReactor
import time

manager = Manager()
lock = manager.Lock()
reactors: dict = {}
result_list = []

async def a_call(x):
    pid = os.getpid()
    try:
        with lock:
            reactor = reactors.get(pid, None)
            if not reactor:
                reactor = NatsReactor()
                reactors[pid] = reactor

        await reactor.connect_nats()
        r = await reactor.aggregate(1000)

    except Exception as e:
        print("Exception:", e)

    # print("pid:", pid, reactors, "reactor:", reactor)
    return r


def foo_pool(x):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(a_call(x))





def log_result(result):
    result_list.append(result)


def apply_async_with_callback():
    start = time.time()
    pool = Pool(processes=10)
    for i in range(1000):
        pool.apply_async(foo_pool, args=(i,), callback=log_result)
    pool.close()
    pool.join()
    dur = 1000 * (time.time() - start)
    print("results:", len(result_list), "took:", dur, "ms")


if __name__ == "__main__":
    apply_async_with_callback()
