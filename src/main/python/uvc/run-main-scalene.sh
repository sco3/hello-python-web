#!/usr/bin/env bash

set -xueo pipefail

poetry run scalene --cli --outfile scalene.out --reduced-profile --no-browser --cpu --profile-interval 10 main_uvicorn.py
