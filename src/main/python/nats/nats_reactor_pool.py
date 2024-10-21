from nats_reactor import NatsReactor
import asyncio
import time


class ConnectionPool:
    def __init__(self, pool_size: int):
        self.pool_size = pool_size
        self._pool: List[NatsReactor] = []
        self._semaphore = asyncio.Semaphore(pool_size)
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize the pool with NATS reactors."""
        async with self._lock:
            self._pool = [NatsReactor(1) for id in range(self.pool_size)]
            await asyncio.gather(*(r.connect_nats() for r in self._pool))

    async def acquire(self):
        """Acquire a reactor from the pool."""
        await self._semaphore.acquire()
        async with self._lock:
            return self._pool.pop()

    async def release(self, reactor: NatsReactor):
        """Release a reactor back to the pool."""
        async with self._lock:
            self._pool.append(reactor)
            self._semaphore.release()


async def worker(task_id: int, pool: ConnectionPool):
    """Worker function to process a task with a reactor from the pool."""
    reactor = await pool.acquire()
    try:
        result = await reactor.aggregate()
        # print(f"Task {task_id} result: {result}")
    finally:
        await pool.release(reactor)


async def main():
    start = time.time()
    num_tasks = 1000
    max_concurrent_tasks = 1

    # Create and initialize the connection pool
    pool = ConnectionPool(pool_size=max_concurrent_tasks)
    await pool.initialize()

    # Create and schedule tasks
    tasks = [worker(task_id, pool) for task_id in range(num_tasks)]

    # Run tasks concurrently and wait for completion
    await asyncio.gather(*tasks)
    print("Took:", 1000 * (time.time() - start), "ms")


if __name__ == "__main__":
    asyncio.run(main())
