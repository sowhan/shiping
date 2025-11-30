"""
Prometheus Metrics Collection
Performance monitoring and KPI tracking.
"""

from prometheus_client import Counter, Histogram, Gauge, Info


# Application info
app_info = Info("maritime_app", "Maritime Route Planning Platform")

# Route calculation metrics
route_calculations_total = Counter(
    "route_calculations_total",
    "Total number of route calculations",
    ["status", "algorithm", "optimization"]
)

route_calculation_duration = Histogram(
    "route_calculation_duration_seconds",
    "Duration of route calculations",
    buckets=[0.1, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]
)

# Cache metrics
cache_hits_total = Counter(
    "cache_hits_total",
    "Total cache hits",
    ["cache_type"]
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total cache misses",
    ["cache_type"]
)

cache_hit_ratio = Gauge(
    "cache_hit_ratio",
    "Current cache hit ratio"
)

# Database metrics
db_connections_active = Gauge(
    "db_connections_active",
    "Number of active database connections"
)

db_query_duration = Histogram(
    "db_query_duration_seconds",
    "Duration of database queries",
    ["query_type"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

# API metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# Port search metrics
port_searches_total = Counter(
    "port_searches_total",
    "Total port search queries"
)

port_search_duration = Histogram(
    "port_search_duration_seconds",
    "Duration of port searches",
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25]
)

# System metrics
active_users = Gauge(
    "active_users",
    "Number of active users"
)


def initialize_metrics() -> None:
    """Initialize application metrics."""
    app_info.info({
        "version": "1.0.0",
        "environment": "production"
    })


def record_route_calculation(
    status: str,
    algorithm: str,
    optimization: str,
    duration: float
) -> None:
    """Record a route calculation metric."""
    route_calculations_total.labels(
        status=status,
        algorithm=algorithm,
        optimization=optimization
    ).inc()
    route_calculation_duration.observe(duration)


def record_cache_operation(cache_type: str, hit: bool) -> None:
    """Record a cache operation."""
    if hit:
        cache_hits_total.labels(cache_type=cache_type).inc()
    else:
        cache_misses_total.labels(cache_type=cache_type).inc()


def record_db_query(query_type: str, duration: float) -> None:
    """Record a database query metric."""
    db_query_duration.labels(query_type=query_type).observe(duration)


def record_http_request(
    method: str,
    endpoint: str,
    status: int,
    duration: float
) -> None:
    """Record an HTTP request metric."""
    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status=str(status)
    ).inc()
    http_request_duration.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)
