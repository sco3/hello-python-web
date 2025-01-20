

set -xueo pipefail

SIZE=${1:-1048664}
MAX=$((1*1048664))
NUM=$(($MAX/$SIZE))
MAX=$(($MAX*15/10))

OUT=$0.out.$SIZE

PORT=9092

JAVA_HOME=~/prg/java-23

KAFKA_HEAP_OPTS=" -Xms1g -Xmx1g "