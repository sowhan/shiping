"""
Unit Tests - Maritime Calculations
Tests for distance, ETA, and fuel calculations.
"""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.maritime import Coordinates, VesselConstraints, VesselType
from app.utils.maritime_calculations import (
    GreatCircleCalculator,
    FuelConsumptionCalculator,
    TransitTimeEstimator,
    calculate_great_circle_distance,
    estimate_fuel_consumption,
    estimate_transit_time
)


class TestGreatCircleCalculations:
    """Tests for great circle distance calculation utilities."""
    
    def test_distance_same_point(self):
        """Distance between same point should be zero."""
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=1.2644, longitude=103.8220)
        
        distance = GreatCircleCalculator.calculate_distance_nautical_miles(origin, destination)
        assert distance == 0.0
    
    def test_distance_known_route(self):
        """Test distance calculation for known route."""
        # Singapore to Rotterdam is approximately 8500 nm (great circle)
        origin = Coordinates(latitude=1.2644, longitude=103.8220)  # Singapore
        destination = Coordinates(latitude=51.9225, longitude=4.4792)  # Rotterdam
        
        distance = GreatCircleCalculator.calculate_distance_nautical_miles(origin, destination)
        assert 5000 < distance < 9000  # Approximate great circle distance
    
    def test_bearing_calculation(self):
        """Test bearing calculation between points."""
        # Singapore to Rotterdam should be roughly northwest
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=51.9225, longitude=4.4792)
        
        bearing = GreatCircleCalculator.calculate_initial_bearing(origin, destination)
        
        # Bearing should be between 0-360
        assert 0 <= bearing < 360
    
    def test_convenience_function(self):
        """Test the convenience function for distance calculation."""
        origin = Coordinates(latitude=1.2644, longitude=103.8220)
        destination = Coordinates(latitude=51.9225, longitude=4.4792)
        
        distance = calculate_great_circle_distance(origin, destination)
        assert distance > 0


class TestFuelConsumptionCalculations:
    """Tests for fuel consumption calculations."""
    
    def test_fuel_consumption_estimation(self):
        """Test fuel consumption estimation."""
        vessel = VesselConstraints(
            vessel_type=VesselType.CONTAINER,
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18,
            deadweight_tonnage=50000
        )
        
        consumption = FuelConsumptionCalculator.estimate_consumption(
            distance_nm=8500,
            vessel_constraints=vessel
        )
        
        # Should be positive and reasonable
        assert consumption > 0
        assert consumption < Decimal('10000')  # Sanity check
    
    def test_convenience_fuel_function(self):
        """Test the convenience function for fuel estimation."""
        vessel = VesselConstraints(
            vessel_type="container",
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18
        )
        
        consumption = estimate_fuel_consumption(1000, vessel)
        assert consumption > 0


class TestTransitTimeEstimation:
    """Tests for transit time estimation."""
    
    def test_transit_time_estimation(self):
        """Test transit time estimation."""
        distance = 8500  # nm
        speed = 18  # knots
        
        transit_time = TransitTimeEstimator.estimate_transit_time(distance, speed)
        
        # At 18 knots, 8500 nm takes ~472 hours plus buffer
        expected_base = 8500 / 18  # ~472 hours
        
        assert float(transit_time) > expected_base  # Should include buffer
        assert float(transit_time) < expected_base * 1.5  # Should not be too much
    
    def test_convenience_transit_function(self):
        """Test the convenience function for transit time."""
        transit_time = estimate_transit_time(1000, 18)
        assert transit_time > 0


class TestCoordinateValidation:
    """Tests for coordinate validation."""
    
    def test_valid_coordinates(self):
        """Valid coordinates should pass validation."""
        # Test valid coordinates
        coord = Coordinates(latitude=45.0, longitude=90.0)
        assert coord.latitude == 45.0
        assert coord.longitude == 90.0
        
        coord2 = Coordinates(latitude=-45.0, longitude=-90.0)
        assert coord2.latitude == -45.0
        
        coord3 = Coordinates(latitude=0.0, longitude=0.0)
        assert coord3.latitude == 0.0
    
    def test_extreme_valid_coordinates(self):
        """Test extreme but valid coordinates."""
        coord_north_pole = Coordinates(latitude=90.0, longitude=0.0)
        assert coord_north_pole.latitude == 90.0
        
        coord_south_pole = Coordinates(latitude=-90.0, longitude=0.0)
        assert coord_south_pole.latitude == -90.0
        
        coord_date_line = Coordinates(latitude=0.0, longitude=180.0)
        assert coord_date_line.longitude == 180.0
