#!/usr/bin/env bash

set -xueo pipefail


cat << 'EOF' > /tmp/run.py
import uvicorn
uvicorn.run(
        "main_uvicorn:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
)
EOF

poetry run \
    scalene --cli --outfile scalene-out --reduced-profile --no-browser --cpu --profile-interval 10 \
    /tmp/run.py
