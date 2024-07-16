#!/usr/bin/env -S poetry run python

from fastapi import FastAPI, WebSocket
import logging
import time
import asyncio
import uvloop
import subprocess


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


logging.basicConfig(level=logging.CRITICAL)

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    # print(f"Received message: {time.time_ns()} {data}")
    await websocket.send_text("Hello, world!\n")
    await websocket.close()


if __name__ == "__main__":

    command = [
        "gunicorn",
        "main_gun:app",
        "-k",
        "uvicorn.workers.UvicornWorker",
        "--bind",
        "0.0.0.0:8081",
        "--log-level",
        "critical",
    ]
    subprocess.run(command)
