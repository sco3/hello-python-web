

set -xueo pipefail

SIZE=${1:-1048664}
MAX=$((20000*1048664))
NUM=$(($MAX/$SIZE))
MAX=$(($MAX*15/10))

OUT=$0.out.$SIZE

