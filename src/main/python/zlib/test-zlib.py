#!/usr/bin/env -S poetry run python


print ("Add psutil with poetry add psutil")


import psutil
import zlib
import time
import gc

process = psutil.Process()
print (process.memory_info().rss // 1024)

obj=[zlib.compressobj() for _ in range (10000)]

del obj

for _ in range (3600):
    print (process.memory_info().rss // 1024)
    gc.collect()
    time.sleep (1)

