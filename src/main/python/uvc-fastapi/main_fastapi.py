#!/usr/bin/env -S poetry run python

import uvicorn
import subprocess
import asyncio
import uvloop
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
async def home():
    return f"Hello, World!\n"


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    n: int = 1
    print(f"workers: {n}")
    uvicorn.run(
        "main_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
        workers=n,
    )
