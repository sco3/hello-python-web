#!/usr/bin/env -S poetry run python

import uvicorn

from typing import ClassVar

data: bytes = b"Hello, World!\n"


class Consts:
    SQUARE: ClassVar[str] = "/square/"
    SQLEN: ClassVar[int] = len(SQUARE)


async def app(scope, receive, send):
    assert scope["type"] == "http"
    path: str = scope["path"]
    body: str = b""
    if path.startswith(Consts.SQUARE):
        snum: str = path[Consts.SQLEN :]
        num: int = int(snum)
        body = str(num * num)

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
            "body": body.encode(),
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main-uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )
