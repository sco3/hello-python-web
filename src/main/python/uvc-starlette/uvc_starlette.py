#!/usr/bin/env -S poetry run python

import uvicorn
import asyncio
import uvloop
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

async def home(request):
    return PlainTextResponse("Hello, World!")

app = Starlette(routes=[
    Route("/", home)
])

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
