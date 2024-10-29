#!/usr/bin/env bash

set -xueo pipefail


cat << 'EOF' > run.py
import uvicorn
uvicorn.run("claude:app",host="0.0.0.0",port=8000,reload=False,log_level="error")
EOF

poetry run \
    scalene --cli --outfile scalene.out \
    --reduced-profile --profile-all --no-browser --cpu --profile-interval 10 \
    run.py
