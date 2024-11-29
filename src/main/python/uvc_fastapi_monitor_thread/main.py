#!/usr/bin/env -S poetry run python

from fastapi import FastAPI, Response

monitor = None
app = FastAPI()

@app.get("/")
async def home():
    result = ""
    if monitor:
       result = monitor.saved_dicts
    return Response(content=result, media_type="text/plain")


