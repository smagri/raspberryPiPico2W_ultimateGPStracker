#!/usr/bin/env python3

import time

# This gives the resolution of time.perf_counter() of your hardware and 0s

# RESULT:

# namespace(implementation='clock_gettime(CLOCK_MONOTONIC)',
# monotonic=True, adjustable=False, resolution=1e-09)

# However — this is just what the underlying system clock reports, not
# what Python can actually measure between two successive calls.

info = time.get_clock_info('perf_counter')
print(info)

