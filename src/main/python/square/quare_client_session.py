#!/usr/bin/env -S poetry run python

import aiohttp
import asyncio
import time


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    # Create a single ClientSession to be reused
    async with aiohttp.ClientSession() as session:
        # Perform multiple requests using the same session
        for i in range(1, 1001):
            url_with_param = f"http://localhost:8000/square/{i}"
            response_text = await fetch(session, url_with_param)
            # print(f"Response for {i}: {response_text}")


if __name__ == "__main__":
    start = time.time()
    for _ in range(1):
        asyncio.run(main())

    print("Took", (time.time() - start) * 1000, "ms")
