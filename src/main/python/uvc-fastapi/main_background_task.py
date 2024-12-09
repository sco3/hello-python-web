#!/usr/bin/env -S uv run

import asyncio
import contextvars
import gc
import threading
import uuid

from fastapi import FastAPI, HTTPException
import uvicorn


app = FastAPI()

state_var = contextvars.ContextVar("state")
tasks = set()


async def simple_task():
    await asyncio.sleep(10)
    print("Simple task", state_var.get())


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


@app.get("/start-task")
async def start_task():
    state_var.set(uuid.uuid4())
    background_task = asyncio.create_task(simple_task())
    background_task.add_done_callback(completion)
    tasks.add(background_task)
    return {"message": state_var.get()}


if __name__ == "__main__":
    threading.Thread(target=count_context_objects, daemon=True).start()
    uvicorn.run(
        "main_background_task:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
