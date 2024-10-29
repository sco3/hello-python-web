#!/usr/bin/env -S poetry run python

import uvicorn
import uvloop
import asyncio
import sys

async def app(scope, receive, send):
    assert scope["type"] == "http"

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": b"Hello, World!\n",
        }
    )


if __name__ == "__main__":
    print (f"python: {sys.version} uvicorn: {uvicorn.__version__} uvloop: {uvloop.__version__} policy: {asyncio.get_event_loop_policy()}")
    uvicorn.run(
        "main_uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )
