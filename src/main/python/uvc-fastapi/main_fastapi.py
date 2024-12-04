#!/usr/bin/env -S uv run

import asyncio
from datetime import datetime
import subprocess
from typing import Annotated, Any, Dict, ClassVar

from fastapi import FastAPI, Depends, Request, WebSocket
import uvicorn
import uvloop


class MyClass:
    counter: ClassVar[int] = 0

    def __init__(self) -> None:
        MyClass.counter += 1
        self.cnt = MyClass.counter

    def clean(self) -> None:
        self.cnt = None
        print("clean", self.cnt)

    @staticmethod
    async def resource():
        print("Resource initialized")
        instance = MyClass()
        try:
            yield instance
        finally:
            instance.clean()
            print("Resource finalized")


app = FastAPI()


@app.middleware("http")
async def filter(request: Request, call_next):
    return await call_next(request)


@app.get("/")
async def home(reso=Depends(MyClass.resource)):
    print("route", reso)
    return f"Hello, World!\n"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    workers: int = 1
    port: int = 8000
    print(f"{port=} {workers=}")
    uvicorn.run(
        "main_fastapi:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="error",
        workers=workers,
    )
