"""
Performance Tests - Route Calculation
Benchmarks for route calculation performance.

Note: These tests benchmark the calculation algorithms without requiring
database or cache infrastructure. Full performance tests should be run
with docker-compose for accurate end-to-end measurements.
"""

import time
import pytest

from app.utils.maritime_calculations import (
    GreatCircleCalculator,
    FuelConsumptionCalculator,
    TransitTimeEstimator
)
from app.models.maritime import Coordinates, VesselConstraints, VesselType


@pytest.mark.performance
class TestCalculationPerformance:
    """Performance tests for maritime calculations."""
    
    def test_distance_calculation_under_1ms(self):
        """Distance calculation should complete under 1ms."""
        origin = Coordinates(latitude=1.2644, longitude=103.8220)  # Singapore
        destination = Coordinates(latitude=51.9225, longitude=4.4792)  # Rotterdam
        
        start_time = time.time()
        
        result = GreatCircleCalculator.calculate_distance_nautical_miles(origin, destination)
        
        duration_ms = (time.time() - start_time) * 1000
        
        assert duration_ms < 1, f"Calculation took {duration_ms}ms, expected < 1ms"
        assert result > 0
    
    def test_bearing_calculation_under_1ms(self):
        """Bearing calculation should complete under 1ms."""
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=51.9225, longitude=4.4792)
        
        start_time = time.time()
        
        result = GreatCircleCalculator.calculate_initial_bearing(origin, destination)
        
        duration_ms = (time.time() - start_time) * 1000
        
        assert duration_ms < 1, f"Calculation took {duration_ms}ms, expected < 1ms"
        assert 0 <= result < 360
    
    def test_fuel_estimation_under_10ms(self):
        """Fuel consumption estimation should complete under 10ms."""
        vessel = VesselConstraints(
            vessel_type=VesselType.CONTAINER,
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18,
            deadweight_tonnage=50000
        )
        
        start_time = time.time()
        
        result = FuelConsumptionCalculator.estimate_consumption(8500, vessel)
        
        duration_ms = (time.time() - start_time) * 1000
        
        assert duration_ms < 10, f"Calculation took {duration_ms}ms, expected < 10ms"
        assert result > 0
    
    def test_transit_time_under_1ms(self):
        """Transit time estimation should complete under 1ms."""
        start_time = time.time()
        
        result = TransitTimeEstimator.estimate_transit_time(8500, 18)
        
        duration_ms = (time.time() - start_time) * 1000
        
        assert duration_ms < 1, f"Calculation took {duration_ms}ms, expected < 1ms"
        assert result > 0


@pytest.mark.performance
class TestBatchPerformance:
    """Batch performance tests."""
    
    def test_multiple_distance_calculations(self):
        """Multiple distance calculations should maintain performance."""
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=51.9225, longitude=4.4792)
        
        calculations = 1000
        start_time = time.time()
        
        for _ in range(calculations):
            GreatCircleCalculator.calculate_distance_nautical_miles(origin, destination)
        
        total_duration_ms = (time.time() - start_time) * 1000
        avg_duration_ms = total_duration_ms / calculations
        
        # Each calculation should average under 1ms (realistic for CI environments)
        assert avg_duration_ms < 1, f"Average calculation took {avg_duration_ms}ms"
        
        # 1000 calculations should complete under 1000ms total
        assert total_duration_ms < 1000, f"Total time was {total_duration_ms}ms"


@pytest.mark.performance
class TestKPICompliance:
    """Tests to verify KPI targets from prompt.md."""
    
    def test_simple_route_calculation_kpi(self):
        """Verify simple route calculations meet <500ms KPI target.
        
        Note: This tests calculation logic only. Full end-to-end
        route calculation with database would be tested with docker-compose.
        """
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=51.9225, longitude=4.4792)
        
        vessel = VesselConstraints(
            vessel_type=VesselType.CONTAINER,
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18,
            deadweight_tonnage=50000
        )
        
        start_time = time.time()
        
        # Simulate full calculation pipeline
        distance = GreatCircleCalculator.calculate_distance_nautical_miles(origin, destination)
        bearing = GreatCircleCalculator.calculate_initial_bearing(origin, destination)
        fuel = FuelConsumptionCalculator.estimate_consumption(distance, vessel)
        transit_time = TransitTimeEstimator.estimate_transit_time(distance, vessel.cruise_speed_knots)
        
        duration_ms = (time.time() - start_time) * 1000
        
        # KPI target is <500ms for simple routes
        assert duration_ms < 500, f"Calculation pipeline took {duration_ms}ms, KPI target is <500ms"
        
        # Verify results are valid
        assert distance > 5000  # Singapore to Rotterdam is ~6000nm
        assert 0 <= bearing < 360
        assert fuel > 0
        assert transit_time > 0
