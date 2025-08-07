node
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     3.55ms   10.65ms 281.57ms   99.11%
    Req/Sec    36.83k     1.72k   39.69k    92.00%
  733064 requests in 10.00s, 126.54MB read
Requests/sec:  73287.36
Transfer/sec:     12.65MB
```

uvicorn
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    13.90ms   25.56ms 637.11ms   99.06%
    Req/Sec     8.40k   546.75    10.31k    79.50%
  167440 requests in 10.01s, 24.11MB read
Requests/sec:  16721.43
Transfer/sec:      2.41MB
```
