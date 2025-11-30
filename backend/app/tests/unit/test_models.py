"""
Unit Tests - Pydantic Models
Tests for data model validation.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.maritime import (
    RouteRequest,
    VesselConstraints,
    Port,
    Coordinates,
    VesselType,
    PortType,
    OperationalStatus,
    OptimizationCriteria
)


class TestCoordinates:
    """Tests for Coordinates model."""
    
    def test_valid_coordinates(self):
        """Valid coordinates should pass validation."""
        coord = Coordinates(latitude=45.0, longitude=90.0)
        assert coord.latitude == 45.0
        assert coord.longitude == 90.0
    
    def test_extreme_coordinates(self):
        """Extreme but valid coordinates should pass."""
        coord_north = Coordinates(latitude=90.0, longitude=0.0)
        assert coord_north.latitude == 90.0
        
        coord_south = Coordinates(latitude=-90.0, longitude=0.0)
        assert coord_south.latitude == -90.0
        
        coord_east = Coordinates(latitude=0.0, longitude=180.0)
        assert coord_east.longitude == 180.0
        
        coord_west = Coordinates(latitude=0.0, longitude=-180.0)
        assert coord_west.longitude == -180.0
    
    def test_invalid_latitude(self):
        """Invalid latitude should fail validation."""
        with pytest.raises(ValidationError):
            Coordinates(latitude=91.0, longitude=0.0)
        
        with pytest.raises(ValidationError):
            Coordinates(latitude=-91.0, longitude=0.0)
    
    def test_invalid_longitude(self):
        """Invalid longitude should fail validation."""
        with pytest.raises(ValidationError):
            Coordinates(latitude=0.0, longitude=181.0)
        
        with pytest.raises(ValidationError):
            Coordinates(latitude=0.0, longitude=-181.0)


class TestVesselConstraints:
    """Tests for VesselConstraints model."""
    
    def test_valid_vessel_constraints(self):
        """Valid vessel constraints should pass validation."""
        constraints = VesselConstraints(
            vessel_type=VesselType.CONTAINER,
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18,
            max_range_nautical_miles=10000,
            fuel_type="vlsfo",
            suez_canal_compatible=True,
            panama_canal_compatible=True
        )
        assert constraints.vessel_type == VesselType.CONTAINER
        assert constraints.length_meters == 300
    
    def test_vessel_type_enum(self):
        """Test vessel type enum values."""
        constraints = VesselConstraints(
            vessel_type="container",  # Should accept string
            length_meters=300,
            beam_meters=45,
            draft_meters=14,
            cruise_speed_knots=18
        )
        assert constraints.vessel_type == VesselType.CONTAINER
    
    def test_invalid_draft(self):
        """Negative draft should fail validation."""
        with pytest.raises(ValidationError):
            VesselConstraints(
                vessel_type=VesselType.CONTAINER,
                length_meters=300,
                beam_meters=45,
                draft_meters=-5,  # Invalid
                cruise_speed_knots=18
            )
    
    def test_invalid_speed(self):
        """Zero speed should fail validation."""
        with pytest.raises(ValidationError):
            VesselConstraints(
                vessel_type=VesselType.CONTAINER,
                length_meters=300,
                beam_meters=45,
                draft_meters=14,
                cruise_speed_knots=0  # Invalid
            )
    
    def test_zero_length(self):
        """Zero length should fail validation."""
        with pytest.raises(ValidationError):
            VesselConstraints(
                vessel_type=VesselType.CONTAINER,
                length_meters=0,  # Invalid
                beam_meters=45,
                draft_meters=14,
                cruise_speed_knots=18
            )


class TestRouteRequest:
    """Tests for RouteRequest model."""
    
    def test_valid_route_request(self):
        """Valid route request should pass validation."""
        request = RouteRequest(
            origin_port_code="SGSIN",
            destination_port_code="NLRTM",
            departure_time=datetime.utcnow(),
            vessel_constraints=VesselConstraints(
                vessel_type=VesselType.CONTAINER,
                length_meters=300,
                beam_meters=45,
                draft_meters=14,
                cruise_speed_knots=18
            ),
            optimization_criteria=OptimizationCriteria.BALANCED
        )
        assert request.origin_port_code == "SGSIN"
        assert request.destination_port_code == "NLRTM"
    
    def test_same_origin_destination(self):
        """Same origin and destination should fail validation."""
        with pytest.raises(ValidationError):
            RouteRequest(
                origin_port_code="SGSIN",
                destination_port_code="SGSIN",  # Same as origin
                departure_time=datetime.utcnow(),
                vessel_constraints=VesselConstraints(
                    vessel_type=VesselType.CONTAINER,
                    length_meters=300,
                    beam_meters=45,
                    draft_meters=14,
                    cruise_speed_knots=18
                )
            )
    
    def test_port_code_uppercase_conversion(self):
        """Port codes should be converted to uppercase."""
        request = RouteRequest(
            origin_port_code="sgsin",  # lowercase
            destination_port_code="nlrtm",  # lowercase
            departure_time=datetime.utcnow(),
            vessel_constraints=VesselConstraints(
                vessel_type=VesselType.CONTAINER,
                length_meters=300,
                beam_meters=45,
                draft_meters=14,
                cruise_speed_knots=18
            )
        )
        assert request.origin_port_code == "SGSIN"
        assert request.destination_port_code == "NLRTM"


class TestPort:
    """Tests for Port model."""
    
    def test_valid_port(self):
        """Valid port data should pass validation."""
        port = Port(
            id=None,
            unlocode="SGSIN",
            name="Singapore",
            country="Singapore",
            coordinates=Coordinates(latitude=1.2644, longitude=103.8220),
            port_type=PortType.CONTAINER_TERMINAL,
            operational_status=OperationalStatus.ACTIVE
        )
        assert port.unlocode == "SGSIN"
        assert port.name == "Singapore"
    
    def test_port_with_facilities(self):
        """Port with facilities should work."""
        port = Port(
            id=None,
            unlocode="SGSIN",
            name="Singapore",
            country="Singapore",
            coordinates=Coordinates(latitude=1.2644, longitude=103.8220),
            port_type=PortType.MULTIPURPOSE,
            facilities={
                "container_terminal": True,
                "bulk_terminal": True
            }
        )
        assert port.facilities["container_terminal"] is True
    
    def test_port_vessel_compatibility(self):
        """Test vessel compatibility check."""
        port = Port(
            id=None,
            unlocode="SGSIN",
            name="Singapore",
            country="Singapore",
            coordinates=Coordinates(latitude=1.2644, longitude=103.8220),
            port_type=PortType.CONTAINER_TERMINAL,
            max_vessel_length_meters=400,
            max_vessel_beam_meters=60,
            max_draft_meters=20
        )
        
        # Should be compatible
        assert port.is_compatible_with_vessel(300, 45, 14) is True
        
        # Should not be compatible (too large)
        assert port.is_compatible_with_vessel(500, 45, 14) is False


class TestOptimizationCriteria:
    """Tests for OptimizationCriteria enum."""
    
    def test_optimization_criteria_values(self):
        """Test all optimization criteria values."""
        assert OptimizationCriteria.FASTEST.value == "fastest"
        assert OptimizationCriteria.MOST_ECONOMICAL.value == "most_economical"
        assert OptimizationCriteria.MOST_RELIABLE.value == "most_reliable"
        assert OptimizationCriteria.BALANCED.value == "balanced"
