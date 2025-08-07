#!/usr/bin/env -S uv run

import asyncio
from blacksheep import Application
from blacksheep.server import Server

app = Application()

@app.route("/")
async def home():
    return b"Hello, World!"

server = Server(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    asyncio.run(server.run())