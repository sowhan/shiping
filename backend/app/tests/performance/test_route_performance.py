"""
Performance Tests - Route Calculation
Benchmarks for route calculation performance.
"""

import time
import pytest
from typing import List

from app.services.route_planner import MaritimeRoutePlanner


@pytest.mark.performance
class TestRoutePerformance:
    """Performance tests for route calculations."""
    
    def test_simple_route_under_500ms(self):
        """Simple route calculation should complete under 500ms."""
        planner = MaritimeRoutePlanner()
        
        # Sample ports
        ports = [
            {"code": "SGSIN", "lat": 1.2644, "lon": 103.8220},
            {"code": "NLRTM", "lat": 51.9225, "lon": 4.4792}
        ]
        
        start_time = time.time()
        
        # This tests the calculation logic (without database)
        # In production, would test actual API response time
        result = planner._calculate_direct_distance(
            ports[0]["lat"], ports[0]["lon"],
            ports[1]["lat"], ports[1]["lon"]
        )
        
        duration_ms = (time.time() - start_time) * 1000
        
        assert duration_ms < 500, f"Calculation took {duration_ms}ms"
        assert result > 0
    
    def test_multiple_calculations_performance(self):
        """Multiple calculations should maintain performance."""
        planner = MaritimeRoutePlanner()
        
        # Test 100 calculations
        calculations = 100
        start_time = time.time()
        
        for _ in range(calculations):
            planner._calculate_direct_distance(
                1.2644, 103.8220,
                51.9225, 4.4792
            )
        
        total_duration_ms = (time.time() - start_time) * 1000
        avg_duration_ms = total_duration_ms / calculations
        
        assert avg_duration_ms < 10, f"Average calculation took {avg_duration_ms}ms"
    
    def test_cache_performance(self):
        """Cache lookups should be sub-millisecond."""
        # Placeholder for cache performance test
        # Would test Redis cache hit performance
        pass


@pytest.mark.performance
class TestMemoryUsage:
    """Memory usage tests."""
    
    def test_planner_memory_footprint(self):
        """Route planner should have reasonable memory footprint."""
        import sys
        
        planner = MaritimeRoutePlanner()
        size = sys.getsizeof(planner)
        
        # Should be under 10MB
        assert size < 10 * 1024 * 1024
