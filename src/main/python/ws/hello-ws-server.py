import asyncio
import websockets

async def hello(websocket, path):
    await websocket.send("Hello World!\n")

start_server = websockets.serve(hello, "localhost", 8081)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()