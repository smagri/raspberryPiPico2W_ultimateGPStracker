#!/usr/bin/env python3


import time

# what Python can actually measure between two successive calls.

# To  see  the  true  practical resolution,  the  smallest  measurable
# interval between two successive calles to time.perf_counter()

# This method  reflects the real  performance limit for your  CPU, OS,
# and Python interpreter — far more useful for timing-sensitive code.

# running this with range(1_000_000) HANGS MY MACHINE

last = time.perf_counter()
min_diff = float('inf')
count = 0

# That  means  your  system  clock  (and  Python’s  perf_counter)  can
# distinguish time  intervals on  the order of  tens of  nanoseconds —
# though  actual precision  is  often coarser  due  to scheduling  and
# hardware timer granularity.

# time.perf_counter() does  not block.   It is just  a high-resolution
# clock that simply returns  a floating-point number-the current value
# of  a monotonic  system  timer(seconds since  an arbirary  reference
# point.)

# What it does:

# Measures  the time  difference (diff)  between consecutive  calls to
# time.perf_counter().

# Tracks  the  smallest  non-zero   difference,  i.e.,  the  practical
# resolution of your timer.

# Reports the smallest detectable interval (in nanoseconds/microseconds).

# Outcome: Tells you how finely your system clock can distinguish time
# intervals  — this  is very  useful  if you  want to  know the  timer
# resolution for high-precision measurements.

# Finds the  fastest “tick” the  timer can report, independent  of how
# fast your CPU  loop runs.  Remember if you have  a fast computer the
# CPU  may happen  so  quickly  that the  system  timer hasn't  ticked
# forward  yet, so  the next  call can  return the  same floatin-point
# value as the previous one.


try:
    for _ in range(1_100_000):
        now = time.perf_counter()
        diff = now - last
        if diff > 0:
            # checks diff > 0 — it only counts intervals where the
            # timer actually advanced.
            min_diff = min(min_diff, diff)
        last = now
        count += 1
except KeyboardInterrupt:
    print("\nInterrupted by user (Ctrl-C).")

# report whatever we have so far
if min_diff < float("inf"):
    print(f"\nSamples collected: {count}")
    print(f"Smallest observed delta: {min_diff*1e9:.1f} ns ({min_diff*1e6:.3f} µs)")
else:
    print("No measurements recorded.")
