#!/usr/bin/env -S uv run

import asyncio
from contextvars import ContextVar, Token
from datetime import datetime
import subprocess
from typing import Annotated, Any, Dict, ClassVar

from fastapi import FastAPI, Depends, Request, WebSocket, WebSocketDisconnect
import anyio
from anycorn import serve
from anycorn.config import Config


class MyClass:
    counter: ClassVar[int] = 0

    def __init__(self) -> None:
        MyClass.counter += 1
        self.cnt = MyClass.counter
        self.token: Token = 0

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
async def home(request:Request,reso=Depends(MyClass.resource)):
    request.state.reso=reso
    print("route", reso)
    return f"Hello, World!\n"+str(request.state.reso)


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, reso=Depends(MyClass.resource)
):
    await websocket.accept()
    websocket.state.asdf="asdf-value"
    websocket.state['user_id'] = "user_123"
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except Exception as ex:
        print("Client disconnected", websocket.state.asdf)


if __name__ == "__main__":

    workers: int = 1
    port: int = 8000
    print(f"{port=} {workers=}")
    anyio.run(
        serve,
        app,
        Config(),
    )
