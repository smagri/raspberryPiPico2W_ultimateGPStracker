#!/usr/bin/env python3


import time

start = time.perf_counter()
for _ in range(1000):
    pass
end = time.perf_counter()

print(f"Loop time: {(end - start) * 1e6:.2f} µs")
