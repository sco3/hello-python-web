#!/usr/bin/env -S poetry run python
import uvicorn

data: bytes = b"Hello, World!\n"


async def app(scope, receive, send):
    assert scope["type"] == "http"
    body = b""

    while True:
        message = await receive()
        if message["type"] == "http.request":
            body += message.get("body", b"")
            if not message.get("more_body"):
                break

    print("Received POST data:", body)

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    if scope.get("path", "") == "/long":
        await send(
            {
                "type": "http.response.body",
                "body": data,
            }
        )
    else:
        await send(
            {
                "type": "http.response.body",
                "body": b"Hello, World!\n",
            }
        )
        

with open("../../../../text-request.txt", "rb") as f:
    data = f.read()


if __name__ == "__main__":
    uvicorn.run(
        "main-uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )
