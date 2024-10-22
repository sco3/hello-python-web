#!/usr/bin/env bash

set -xueo pipefail


cat << 'EOF' > run.py
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
    pyinstrument \
    /tmp/run.py
