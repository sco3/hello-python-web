fastwsgi
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   784.94us   93.02us   3.11ms   94.17%
    Req/Sec   128.11k     5.33k  136.77k    82.00%
  2547947 requests in 10.00s, 340.19MB read
Requests/sec: 254749.13
Transfer/sec:     34.01MB
```

uvicorn
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    14.41ms  676.05us  19.81ms   84.16%
    Req/Sec     6.97k   279.14     7.70k    79.00%
  138704 requests in 10.00s, 19.97MB read
Requests/sec:  13865.62
Transfer/sec:      2.00MB
```

minihttp
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   273.32us  102.32us   3.75ms   85.70%
    Req/Sec   193.81k    15.74k  250.57k    87.00%
  3854999 requests in 10.00s, 371.32MB read
Requests/sec: 385441.12
Transfer/sec:     37.13MB
```

JavaJooby
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.94ms    3.85ms  88.62ms   97.94%
    Req/Sec   133.53k    37.91k  180.86k    78.00%
  2657596 requests in 10.00s, 321.88MB read
Requests/sec: 265700.85
Transfer/sec:     32.18MB
```
