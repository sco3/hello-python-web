#!/usr/bin/env -S uv run

import asyncio
import contextvars
import gc
import threading
import uuid

from fastapi import FastAPI, HTTPException, Request
import uvicorn


app = FastAPI()

state_var = contextvars.ContextVar("state")
tasks = set()

class State:
    def __init__ (self):
        self.state = ["?"]

    def __str__ (self):
        return str(self.state)


async def simple_task():
    await asyncio.sleep(10)
    state_var.get().state.append(uuid.uuid4())
    print("Simple task", str(state_var.get()))


def count_context_objects():
    while True:
        context_count = 0
        tasks = 0
        for obj in gc.get_objects():
            if isinstance(obj, contextvars.Context):
                context_count += 1

            if isinstance(obj, asyncio.Task):
                tasks += 1

        print(f"Number of Context objects: {context_count} tasks: {tasks}")
        asyncio.run(asyncio.sleep(5))


def completion(task: asyncio.Task):
    tasks.discard(task)


@app.middleware("http")
async def mw(request: Request, call_next):
    state = State()
    state.state.append(uuid.uuid4())
    state_var.set(state)
    return await call_next(request)


@app.get("/start-task")
async def start_task():
    background_task = asyncio.create_task(simple_task())
    background_task.add_done_callback(completion)
    tasks.add(background_task)
    return {"message": state_var.get()}


if __name__ == "__main__":
    state = State()
    print (state)
    threading.Thread(target=count_context_objects, daemon=True).start()
    uvicorn.run(
        "main_background_task:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
