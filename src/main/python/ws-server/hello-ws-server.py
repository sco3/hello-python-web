#!/usr/bin/env -S poetry run python 


import asyncio
import websockets
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def hello(websocket, path):
    async for message in websocket:
        #print(f"{message}")
        await websocket.send("Hello, world!\n")

start_server = websockets.serve(hello, "localhost", 8081)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()