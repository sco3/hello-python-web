import asyncio
import websockets


async def websocket_client():
    uri = "ws://localhost:8081/ws"
    async with websockets.connect(uri) as websocket:
        # Send a message to the server
        await websocket.send("Hello, server!")

        # Receive and print the response from the server
        response = await websocket.recv()
        print(f"Response from server: {response}")


asyncio.get_event_loop().run_until_complete(websocket_client())
