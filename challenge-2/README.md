# Requirement
Compares block numbers between two Ethereum providers (Ankr and Infura)
   - if Ankr blocknumber - Infura blocknumber < 5 => success
   - else => fail

# Run local 
```shell
pip install flask requests python-dotenv
pỵthon app.py
```

# Run with docker compose
```shell
docker-compose up --build
```

# Test
```shell
curl http://localhost:5000/block_diff_status
```

# Bonus: export metrics to prometheus
Use the file app-metrics.py instead of the file app.py (overwrite app-metrics.py to app.py if build docker image)

Check:
```shell
curl http://localhost:5000/targets
curl http://localhost:5000/metrics
```

Build Docker and deploy to k8s:
```shell
docker build -f Dockerfile -t asia-southeast1-docker.pkg.dev/[PROJECT]/[REPOS]/[IMAGE]:[TAG] .
docker push asia-southeast1-docker.pkg.dev/[PROJECT]/[REPOS]/[IMAGE]:[TAG]
kubectl apply -f http-sd-endpoint.yaml -n demo
```

Configure prometheus:
```
  - job_name: "check-block-diff-metrics"
    scrape_interval: 30s
    metrics_path: /metrics
    scheme : http
    http_sd_configs:
      - url: http://http-sd-endpoint.demo:5000/targets
        refresh_interval: 60s
```

Alerts rule:
```
groups:
  - name: Block Difference Alerts
    rules:
      - alert: BlockDifferenceTooHigh
        expr: block_diff > 5
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Block difference between Infura and Ankr is too high"
          description: "The block difference is {{ $value }} blocks, which is greater than 5."
      # OR
      - alert: BlockStatusFail
        expr: block_diff_status == 0
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "Block status check failed"
          description: "The block difference status is {{ $value }}, indicating that the block difference is too high or status check failed."

```