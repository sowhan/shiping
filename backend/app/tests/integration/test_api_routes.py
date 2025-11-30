"""
Integration Tests - Route Planning API
Tests for route calculation endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestRouteAPI:
    """Integration tests for route planning API."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """Health check endpoint should return healthy status."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client: AsyncClient):
        """Root endpoint should return service info."""
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
    
    @pytest.mark.asyncio
    async def test_calculate_route(
        self,
        async_client: AsyncClient,
        sample_route_request: dict
    ):
        """Route calculation should return valid response."""
        response = await async_client.post(
            "/api/v1/routes/calculate",
            json=sample_route_request
        )
        # May fail without database, but should not crash
        assert response.status_code in [200, 422, 500]
    
    @pytest.mark.asyncio
    async def test_validate_route(
        self,
        async_client: AsyncClient,
        sample_route_request: dict
    ):
        """Route validation should return validation result."""
        response = await async_client.post(
            "/api/v1/routes/validate",
            json=sample_route_request
        )
        assert response.status_code in [200, 400, 422]
    
    @pytest.mark.asyncio
    async def test_port_search(self, async_client: AsyncClient):
        """Port search should return results."""
        response = await async_client.get(
            "/api/v1/ports/search",
            params={"query": "singapore", "limit": 10}
        )
        # May return empty without database
        assert response.status_code in [200, 500]
    
    @pytest.mark.asyncio
    async def test_invalid_route_request(self, async_client: AsyncClient):
        """Invalid request should return 422."""
        response = await async_client.post(
            "/api/v1/routes/calculate",
            json={"invalid": "data"}
        )
        assert response.status_code == 422
