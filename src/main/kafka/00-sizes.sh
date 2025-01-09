

set -xueo pipefail

SIZE=${1:-1048664}
MAX=100G
NUM=200000

OUT=$0.out.$SIZE

if [ "$1" -gt 100000 ] ; then
    NUM=$((NUM/10))
fi
