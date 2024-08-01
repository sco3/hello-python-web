#!/usr/bin/env -S poetry run python


import asyncio
import aiohttp
import time


async def fetch(session: aiohttp.ClientSession, i: int) -> None:
    url = f"http://localhost:8000/square/{i}"
    async with session.get(url) as response:
        if response.status == 200:
            result = await response.text()
            # print(f"Response for {i}: {result}")
        else:
            print(f"Failed to fetch {url}. Status code: {response.status}")


async def main() -> None:

    num_requests = 1000
    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks
        tasks = [fetch(session, i) for i in range(1, num_requests + 1)]
        # Run tasks concurrently
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    for _ in range(1):
        asyncio.run(main())

    print("Took", (time.time() - start) * 1000, "ms")
