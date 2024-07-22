#!/usr/bin/env -S poetry run python

import fastwsgi

prefix="/api/square/unary/"
prefix_len=len(prefix)

def app(environ, start_response):

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    headers = [("Content-Type", "text/plain")]
    start_response("200 OK", headers)
    path = environ.get("PATH_INFO", "")
    if not path == "":
        v = int(path[prefix_len:])

    return [str(v * v).encode()]


if __name__ == "__main__":
    fastwsgi.run(wsgi_app=app, host="0.0.0.0", port=7576)
