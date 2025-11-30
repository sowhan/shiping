"""
Unit Tests - Maritime Calculations
Tests for distance, ETA, and fuel calculations.
"""

import pytest
from datetime import datetime, timedelta

from app.utils.maritime_calculations import MaritimeCalculator


class TestMaritimeCalculations:
    """Tests for maritime calculation utilities."""
    
    def test_haversine_distance_same_point(self):
        """Distance between same point should be zero."""
        distance = MaritimeCalculator.haversine_distance(
            lat1=1.2644, lon1=103.8220,
            lat2=1.2644, lon2=103.8220
        )
        assert distance == 0.0
    
    def test_haversine_distance_known_route(self):
        """Test distance calculation for known route."""
        # Singapore to Rotterdam is approximately 8500 nm
        distance = MaritimeCalculator.haversine_distance(
            lat1=1.2644, lon1=103.8220,  # Singapore
            lat2=51.9225, lon2=4.4792     # Rotterdam
        )
        assert 5000 < distance < 9000  # Approximate great circle distance
    
    def test_calculate_eta(self):
        """Test ETA calculation."""
        departure = datetime(2024, 1, 20, 8, 0, 0)
        distance = 8500  # nm
        speed = 18  # knots
        
        eta = MaritimeCalculator.calculate_eta(distance, speed, departure)
        
        # At 18 knots, 8500 nm takes ~472 hours
        expected_duration = timedelta(hours=8500/18)
        expected_eta = departure + expected_duration
        
        assert eta == expected_eta
    
    def test_estimate_fuel_consumption(self):
        """Test fuel consumption estimation."""
        consumption = MaritimeCalculator.estimate_fuel_consumption(
            distance_nm=8500,
            vessel_type="container",
            speed_knots=18
        )
        
        # Should be positive and reasonable
        assert consumption > 0
        assert consumption < 10000  # Sanity check
    
    def test_bearing_calculation(self):
        """Test bearing calculation between points."""
        # Singapore to Rotterdam should be roughly northwest
        bearing = MaritimeCalculator.calculate_bearing(
            lat1=1.2644, lon1=103.8220,
            lat2=51.9225, lon2=4.4792
        )
        
        # Bearing should be between 0-360
        assert 0 <= bearing < 360


class TestCoordinateValidation:
    """Tests for coordinate validation."""
    
    def test_valid_coordinates(self):
        """Valid coordinates should pass."""
        assert MaritimeCalculator.validate_coordinates(45.0, 90.0) is True
        assert MaritimeCalculator.validate_coordinates(-45.0, -90.0) is True
        assert MaritimeCalculator.validate_coordinates(0.0, 0.0) is True
    
    def test_invalid_latitude(self):
        """Invalid latitude should fail."""
        assert MaritimeCalculator.validate_coordinates(91.0, 0.0) is False
        assert MaritimeCalculator.validate_coordinates(-91.0, 0.0) is False
    
    def test_invalid_longitude(self):
        """Invalid longitude should fail."""
        assert MaritimeCalculator.validate_coordinates(0.0, 181.0) is False
        assert MaritimeCalculator.validate_coordinates(0.0, -181.0) is False
