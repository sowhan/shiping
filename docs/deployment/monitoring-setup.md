# Monitoring Setup

## Overview

The Maritime Route Planning Platform uses a comprehensive monitoring stack:

- **Prometheus** - Metrics collection and alerting
- **Grafana** - Visualization and dashboards
- **Jaeger** - Distributed tracing
- **CloudWatch/ELK** - Centralized logging

## Prometheus Configuration

### prometheus.yml

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'maritime-backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: /metrics
    
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    
  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Alert Rules

```yaml
# alerts.yml
groups:
  - name: maritime-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowRouteCalculations
        expr: histogram_quantile(0.95, rate(route_calculation_duration_seconds_bucket[5m])) > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Route calculations are slow"
          
      - alert: LowCacheHitRatio
        expr: rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m])) < 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Cache hit ratio below 80%"
```

## Grafana Dashboards

### Maritime Operations Dashboard

Key panels:
- Route calculations per minute
- Average calculation time (95th percentile)
- Cache hit ratio
- Active users
- Error rate by endpoint

### System Health Dashboard

Key panels:
- CPU usage per service
- Memory usage
- Database connections
- Redis memory usage
- Network I/O

## Application Metrics

### Backend Metrics Endpoint

```python
# Exposed at /metrics
from prometheus_client import Counter, Histogram, Gauge

# Route calculation metrics
route_calculations = Counter(
    'route_calculations_total',
    'Total route calculations',
    ['status', 'algorithm']
)

calculation_duration = Histogram(
    'route_calculation_duration_seconds',
    'Route calculation duration',
    buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

# Cache metrics
cache_hits = Counter('cache_hits_total', 'Cache hits')
cache_misses = Counter('cache_misses_total', 'Cache misses')

# System metrics
active_connections = Gauge(
    'db_active_connections',
    'Active database connections'
)
```

## Logging

### Structured Logging Format

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "maritime-backend",
  "correlation_id": "abc-123",
  "message": "Route calculated successfully",
  "metadata": {
    "origin": "SGSIN",
    "destination": "NLRTM",
    "duration_ms": 245
  }
}
```

### Log Aggregation

```yaml
# Fluentd configuration
<source>
  @type forward
  port 24224
</source>

<match maritime.**>
  @type elasticsearch
  host elasticsearch
  port 9200
  logstash_format true
  logstash_prefix maritime-logs
</match>
```

## Alerting

### Notification Channels

- **Slack** - Warnings and critical alerts
- **PagerDuty** - Critical alerts (24/7)
- **Email** - Daily summary reports

### Alert Escalation

| Severity | Response Time | Escalation |
|----------|--------------|------------|
| Critical | 15 minutes | PagerDuty + Slack |
| Warning | 1 hour | Slack |
| Info | Next business day | Email |

## Health Checks

```bash
# Check all services
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "database": "connected",
  "cache": "connected",
  "uptime_seconds": 86400,
  "version": "1.0.0"
}
```

## Troubleshooting

### High Latency

1. Check Grafana latency dashboard
2. Review slow query logs
3. Check cache hit ratio
4. Verify database connection pool

### Memory Issues

1. Check container memory limits
2. Review Redis memory usage
3. Analyze heap dumps if needed

### Database Issues

1. Check connection pool status
2. Review slow query logs
3. Verify disk space
