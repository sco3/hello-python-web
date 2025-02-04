#!/usr/bin/env -S poetry run python

import uvicorn
import uvloop
import asyncio
import sys


async def app(scope, receive, send):

    await send({
        'type': 'http.response.start',
        'status': 200
    })

    await send({
        'type': 'http.response.body',
        'body': b'Hello, World!\n'
    })



if __name__ == "__main__":
    uvicorn.run(
        "main_uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )
