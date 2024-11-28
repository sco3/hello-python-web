#!/usr/bin/env -S poetry run python

import asyncio
import subprocess
from datetime import datetime

import uvicorn
import uvloop
from fastapi import FastAPI, Response

import monitor

app = FastAPI()


@app.get("/")
async def home():
    result = monitor.endpoint()
    return Response(content=result, media_type="text/plain")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    n: int = 1
    print(f"workers: {n}")
    uvicorn.run(
        "main_fastapi_monitor:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
        workers=n,
    )
