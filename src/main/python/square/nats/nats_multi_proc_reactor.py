import asyncio
from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing.managers import DictProxy
from multiprocessing.managers import ValueProxy
import os
import time

from nats_reactor import NatsReactor


lock = Manager().Lock()
reactors: dict = {}
result_list = []


async def aggregate_async(x: int) -> list:
    pid = os.getpid()
    try:
        reactor = reactors.get(pid, None)
        if not reactor:
            reactor = NatsReactor()
            reactors[pid] = reactor

            with lock:
                print(f"Process: {pid} reactor: {reactor}")

        await reactor.connect_nats()
        result_list = await reactor.aggregate(x)

    except Exception as e:
        print("Exception:", e)

    return result_list


def aggregate_sync(x: int) -> list:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(aggregate_async(x))


def collect_results(result: list) -> None:
    result_list.append(result)


def apply_async_with_callback():
    start = time.time()
    pool = Pool(processes=16)
    for i in range(1000):
        pool.apply_async(aggregate_sync, args=(1000,), callback=collect_results)
    pool.close()
    pool.join()
    dur = 1000 * (time.time() - start)
    print("results:", len(result_list), "took:", dur, "ms")


if __name__ == "__main__":
    apply_async_with_callback()
