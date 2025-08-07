#!/usr/bin/env -S uv run

import uvicorn
import subprocess
from datetime import datetime

from blacksheep import Application, get


app = Application()


@get("/")
async def home():
    return f"Hello, World!\n"


if __name__ == "__main__":

    command = [
        "uvicorn",
        "main_blacksheep:app",
        "--port",
        "8000",
        "--host",
        "0.0.0.0",
        "--log-level",
        "critical",
    ]
    subprocess.run(command)
