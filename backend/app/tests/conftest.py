"""
Test Configuration
Pytest fixtures and test database setup.
"""

import asyncio
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for API testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_route_request() -> dict:
    """Sample route calculation request."""
    # Use future departure time to pass validation
    departure_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    return {
        "origin_port_code": "SGSIN",
        "destination_port_code": "NLRTM",
        "departure_time": departure_time,
        "vessel_constraints": {
            "vessel_type": "container",
            "length_meters": 300,
            "beam_meters": 45,
            "draft_meters": 14,
            "cruise_speed_knots": 18,
            "max_range_nautical_miles": 10000,
            "fuel_type": "vlsfo",
            "suez_canal_compatible": True,
            "panama_canal_compatible": True
        },
        "optimization_criteria": "balanced",
        "include_alternative_routes": True,
        "max_alternative_routes": 3
    }


@pytest.fixture
def sample_port() -> dict:
    """Sample port data."""
    return {
        "id": None,
        "unlocode": "SGSIN",
        "name": "Singapore",
        "country": "Singapore",
        "coordinates": {
            "latitude": 1.2644,
            "longitude": 103.8220
        },
        "port_type": "container_terminal",
        "operational_status": "active"
    }


@pytest.fixture
def sample_vessel_constraints() -> dict:
    """Sample vessel constraints."""
    return {
        "vessel_type": "container",
        "length_meters": 300,
        "beam_meters": 45,
        "draft_meters": 14,
        "cruise_speed_knots": 18
    }
