import requests
import time
import aiohttp
import asyncio

from itertools import product


def get_square(number: int):
    # Define the URL with the path parameter
    url = f"http://localhost:8000/square/{number}"

    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            return data
        else:
            # Handle errors
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            return None
    except requests.RequestException as e:
        # Handle exceptions during the request
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    start: int = time.time()

    calls: int = 1000
    runs: int = 1
    cnt: int = 0

    for run, number in product(range(1, runs + 1), range(1, calls + 1)):
        # print(run, number)
        result = get_square(number)
        cnt += 1

    print("cnt", cnt)

    duration: int = time.time() - start
    rps: int = runs * calls / duration
    print(f"duration: {duration*1000} ms requests: {rps} per second")
