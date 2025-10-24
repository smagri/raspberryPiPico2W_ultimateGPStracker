#!/usr/bin/env python3

What it does:

# Calls time.perf_counter()  1,000,000 times but does  not measure the
# interval between successive calls.

# Measures the total time it takes to execute all 1,000,000 calls.

# Prints the sum total of time for all calls.

# Outcome: Gives you aggregate overhead of calling time.perf_counter()
# repeatedly.  It  does not  tell  you  the smallest  detectable  time
# interval — only how long the calls take in bulk.



# Key point: calling time.perf_counter() repeatedly:

# time.perf_counter()  is just  reading a  system timer  — it  doesn’t
# block, it doesn’t sleep.

# When it returns, the OS doesn’t have to do anything special. The CPU
# keeps executing the next instruction immediately.

# If your CPU is  very fast, the next call may  happen so quickly that
# the system  timer hasn’t ticked  forward yet,  so the next  call can
# return the same floating-point value as the previous one.

# This is  exactly why  Program 2  checks diff  > 0  — it  only counts
# intervals where the timer actually advanced.

import time

start = time.perf_counter()
for _ in range(1000000):
    time.perf_counter()
end = time.perf_counter()
print((end - start) * 1e6, "microseconds total")
