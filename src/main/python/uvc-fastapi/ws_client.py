#!/usr/bin/env -S uv run

import asyncio
import websockets

async def connect():
    uri = "ws://localhost:8000/ws"  # The URI of your WebSocket server
    async with websockets.connect(uri) as websocket:
        print("Connected to the WebSocket server")

        # Send a message to the server
        await websocket.send("Hello, Server!")
        print("Message sent to the server")

        # Receive a message from the server
        response = await websocket.recv()
        print(f"Message received from the server: {response}")

        # Close the WebSocket connection
        await websocket.close()



# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(connect())
