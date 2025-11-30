"""
Test Configuration
Pytest fixtures and test database setup.
"""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
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
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_route_request() -> dict:
    """Sample route calculation request."""
    return {
        "origin_port_code": "SGSIN",
        "destination_port_code": "NLRTM",
        "departure_time": "2024-01-20T08:00:00Z",
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
        "id": 1,
        "unlocode": "SGSIN",
        "name": "Singapore",
        "country": "Singapore",
        "coordinates": {
            "latitude": 1.2644,
            "longitude": 103.8220
        },
        "port_type": "major_hub",
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
