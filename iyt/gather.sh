mkdir -pv csv
FILE=csv/$(date '+%Y%m%d_%H%M%S_%N').csv
banner --color yellow $FILE
time ./history --csv > $FILE
