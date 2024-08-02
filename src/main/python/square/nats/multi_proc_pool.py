from multiprocessing import Pool, Manager
import os
import time
import asyncio
from nats_reactor import NatsReactor


class MultiProcessor:
    def __init__(self, num_processes=None):
        self.num_processes = num_processes or os.cpu_count()
        self.results = []
        self.manager = Manager()
        self.manager.Value ()

    async def execute(self, name):
        reactor = self.manager.Value ("reactor")
        if not reactor:
            reactor = NatsReactor()
            reactor.connect_nats()
            self.storage.reactor = reactor

        reactor = self.storage.reactor
        return reactor.aggregate(1000)

    def wrapper(self, name):
        print("enter:", os.getpid())
        loop = asyncio.get_event_loop()
        r = loop.run_until_complete(self.execute(name))
        print(r)
        return r

    def collect(self, result):
        self.results.append(result)

    def run(self):
        tic = time.time()
        with Pool(processes=self.num_processes) as pool:
            for i in range(10):
                pool.apply_async(self.wrapper, args=(f"x{i}",), callback=self.collect)

            pool.close()
            pool.join()

        print(self.results)
        toc = time.time()
        print(f"Completed in {toc - tic} seconds")


if __name__ == "__main__":
    processor = MultiProcessor()
    processor.run()
