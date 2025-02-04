#!/usr/bin/env -S uv run

import asyncio
from fastapi import FastAPI
import uvicorn



app = FastAPI()


@app.get("/")
async def home():
    return f"Hello, World!\n"


if __name__ == "__main__":

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
