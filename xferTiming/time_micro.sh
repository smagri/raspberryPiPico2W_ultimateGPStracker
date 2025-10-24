##!/usr/bin/env bash

#
# time_micro.sh — measure elapsed wall-clock time with microsecond precision
#

# $# number of arguments passes to the script
if [ $# -eq 0 ]; then
    echo "Usage: time_micro command [args...]"
    return 1
fi

# seconds since epoch with microsecond precision (first 6 digits of nanoseconds)
start=$(date +%s%6N)

# all script arguments, safely quoted
"$@"

end=$(date +%s%6N)

elapsed=$((end - start))
seconds=$((elapsed / 1000000))
microseconds=$((elapsed % 1000000))
echo "Elapsed: ${seconds}s ${microseconds}μs"
