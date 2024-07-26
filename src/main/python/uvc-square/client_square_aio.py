import aiohttp
import asyncio
import time
from itertools import product


async def fetch(url: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def call(i: int) -> int:
    url: str = f"http://localhost:8000/square/{i}"
    out: int = await fetch(url)
    return int(out)


async def main():
    # Example usage
    start: int = time.time_ns()
    calls: int = 1000
    runs: int = 100

    for run, number in product(range(1, runs), range(1, calls)):
        result: int = await call(number)
        # print(f"{number}^2 -> {result}")
        assert result == number * number

    duration: int = time.time_ns() - start
    print(f"duration: {duration/1000_000} ms ")


if __name__ == "__main__":
    asyncio.run(main())
