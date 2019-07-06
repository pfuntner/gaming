set -x
mkdir -pv csv
./history --csv > csv/$(date '+%Y%m%d_%H%M%S_%N').csv
