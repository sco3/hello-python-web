#!/usr/bin/env -S poetry run python

import uvicorn
import asyncio
import json
from typing import Any, Dict, Callable, Awaitable


async def app(
    scope: Dict[str, Any],
    receive: Callable[[], Awaitable[Dict[str, Any]]],
    send: Callable[[Dict[str, Any]], Awaitable[None]],
) -> None:
    assert scope["type"] == "http"

    body: bytes = b""
    while True:
        message: Dict[str, Any] = await receive()
        if message["type"] == "http.request":
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break

    data: Dict[str, Any] = json.loads(body)
    numbers: list[int] = data["numbers"]
    response_body: bytes = f"{len(numbers)}\n".encode("utf-8")

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
            "body": response_body,
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main_uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )
