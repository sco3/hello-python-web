#!/usr/bin/env -S bash




poetry run uvicorn main:app --host 0.0.0.0 --port 8081 --log-level error