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

JerseyNetty
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     8.99ms   21.16ms 516.58ms   94.00%
    Req/Sec    21.24k    11.75k   45.90k    61.00%
  424321 requests in 10.05s, 42.09MB read
Requests/sec:  42238.90
Transfer/sec:      4.19MB
```

JerseyGrizzly
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.86ms    1.99ms  41.48ms   87.93%
    Req/Sec    47.78k    14.62k   73.36k    68.50%
  951798 requests in 10.02s, 72.68MB read
Requests/sec:  95014.39
Transfer/sec:      7.26MB
```

JerseyJetty
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     7.56ms   28.40ms 457.55ms   96.51%
    Req/Sec    36.31k    25.16k   84.63k    54.04%
  716496 requests in 10.05s, 107.96MB read
Requests/sec:  71306.70
Transfer/sec:     10.74MB
```

Vertx
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.08ms    3.78ms  91.07ms   98.88%
    Req/Sec   131.20k    27.87k  155.52k    92.00%
  2608256 requests in 10.00s, 196.51MB read
Requests/sec: 260789.43
Transfer/sec:     19.65MB
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


rust-minihttp
---

```
Running 10s test @ http://127.0.0.1:8000
  2 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   273.46us  101.65us   2.79ms   85.69%
    Req/Sec   193.45k    16.15k  246.23k    84.00%
  3850709 requests in 10.00s, 370.90MB read
Requests/sec: 385038.33
Transfer/sec:     37.09MB
```
