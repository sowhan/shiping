#!/usr/bin/env python
"""
Performance Benchmark Script
Run performance tests and generate report.
"""

import time
import statistics
from app.services.route_planner import MaritimeRoutePlanner


def benchmark_route_calculations(iterations: int = 100):
    """Benchmark route calculation performance."""
    planner = MaritimeRoutePlanner()
    times = []
    
    print(f"Running {iterations} route calculations...")
    
    for i in range(iterations):
        start = time.time()
        planner._calculate_direct_distance(
            1.2644, 103.8220,  # Singapore
            51.9225, 4.4792    # Rotterdam
        )
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)
        
        if (i + 1) % 10 == 0:
            print(f"  Completed {i + 1}/{iterations}")
    
    print("\nResults:")
    print(f"  Mean: {statistics.mean(times):.2f}ms")
    print(f"  Median: {statistics.median(times):.2f}ms")
    print(f"  Std Dev: {statistics.stdev(times):.2f}ms")
    print(f"  Min: {min(times):.2f}ms")
    print(f"  Max: {max(times):.2f}ms")
    print(f"  P95: {sorted(times)[int(len(times) * 0.95)]:.2f}ms")
    print(f"  P99: {sorted(times)[int(len(times) * 0.99)]:.2f}ms")
    
    # Check KPI compliance
    p95 = sorted(times)[int(len(times) * 0.95)]
    if p95 < 500:
        print("\n✅ KPI PASSED: P95 < 500ms")
    else:
        print(f"\n❌ KPI FAILED: P95 = {p95:.2f}ms (target: <500ms)")


if __name__ == "__main__":
    benchmark_route_calculations()
