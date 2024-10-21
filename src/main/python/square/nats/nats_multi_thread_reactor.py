import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
import threading

from nats_reactor import NatsReactor

# Thread-safe storage for reactors and results
reactors = {}
result_list = []
lock = threading.Lock()


async def aggregate_async(x: int) -> list:
    pid = threading.get_native_id()
    try:
        with lock:
            reactor = reactors.get(pid, None)
            if not reactor:
                reactor = NatsReactor()
                reactors[pid] = reactor
                print(f"Thread: {pid} reactor: {reactor}")

        await reactor.connect_nats()
        result_list = await reactor.aggregate(x)

    except Exception as e:
        print("Exception:", e)

    return result_list


def aggregate_sync(x: int) -> list:
    if asyncio.get_event_loop_policy()._local._loop:
        loop = asyncio.get_event_loop()
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(aggregate_async(x))


def collect_results(result: list) -> None:
    with lock:
        result_list.append(result)


def benchmark():
    start = time.time()
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(aggregate_sync, 1000) for _ in range(1000)]
        for future in as_completed(futures):
            collect_results(future.result())

    dur = 1000 * (time.time() - start)
    result_sizes = set()
    for result in result_list:
        result_sizes.add(len(result))
    print("took:", dur, "results:", len(result_list), "sizes:", result_sizes, "ms")


if __name__ == "__main__":
    benchmark()
