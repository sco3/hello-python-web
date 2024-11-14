#!/usr/bin/env -S bash




poetry run granian --host 0.0.0.0 --port 8081 --interface asgi --workers 1  --interface asgi main:app