#!/usr/bin/env -S poetry run python

import fastwsgi
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    fastwsgi.run(app, host='0.0.0.0', port=8000)
