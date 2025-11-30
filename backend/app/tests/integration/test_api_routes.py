"""
Integration Tests - Route Planning API
Tests for route calculation endpoints.

Note: These tests run against the API without a database connection.
Only endpoints that don't require database/cache are tested here.
Full integration tests should be run with docker-compose.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.integration
class TestRouteAPI:
    """Integration tests for route planning API - no infrastructure required."""
    
    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """Health check endpoint should return status regardless of db connection."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        # Status may be 'healthy' or 'degraded' depending on DB/cache availability
        assert data["status"] in ["healthy", "degraded"]
        assert "version" in data
        assert "timestamp" in data
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client: AsyncClient):
        """Root endpoint should return service info."""
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "operational"
    
    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, async_client: AsyncClient):
        """Metrics endpoint should return performance metrics."""
        response = await async_client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "performance_metrics" in data
        assert "system_reliability" in data
        assert "business_kpis" in data
        
        # Verify KPI targets are documented
        perf = data["performance_metrics"]
        assert "route_calculations" in perf
        assert perf["route_calculations"]["target_simple_route_ms"] == 500
        assert perf["route_calculations"]["target_complex_route_ms"] == 3000
        
        assert "caching" in perf
        assert perf["caching"]["target_hit_ratio_percent"] == 95
        
        assert "database" in perf
        assert perf["database"]["target_port_search_ms"] == 100
        
        assert "concurrency" in perf
        assert perf["concurrency"]["target_concurrent_users"] == 10000
    
    @pytest.mark.asyncio
    async def test_openapi_docs_available(self, async_client: AsyncClient):
        """OpenAPI documentation should be available."""
        response = await async_client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        
        # Verify key endpoints are documented
        paths = data["paths"]
        assert "/health" in paths
        assert "/metrics" in paths
        assert "/" in paths


@pytest.mark.integration
class TestHealthEndpoint:
    """Detailed tests for the health endpoint."""
    
    @pytest.mark.asyncio
    async def test_health_returns_all_fields(self, async_client: AsyncClient):
        """Health check should return all required fields."""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Required fields
        assert "status" in data
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data
        assert "uptime_seconds" in data
        assert "database_connected" in data
        assert "cache_connected" in data
    
    @pytest.mark.asyncio
    async def test_health_uptime_is_positive(self, async_client: AsyncClient):
        """Health check uptime should be non-negative."""
        response = await async_client.get("/health")
        data = response.json()
        assert data["uptime_seconds"] >= 0


@pytest.mark.integration  
class TestMetricsEndpoint:
    """Detailed tests for the metrics endpoint."""
    
    @pytest.mark.asyncio
    async def test_metrics_kpi_compliance_fields(self, async_client: AsyncClient):
        """Metrics should include KPI compliance indicators."""
        response = await async_client.get("/metrics")
        data = response.json()
        
        route_calc = data["performance_metrics"]["route_calculations"]
        assert "kpi_compliance" in route_calc
        
        caching = data["performance_metrics"]["caching"]
        assert "kpi_compliance" in caching
    
    @pytest.mark.asyncio
    async def test_metrics_business_kpis_documented(self, async_client: AsyncClient):
        """Metrics should document business KPIs."""
        response = await async_client.get("/metrics")
        data = response.json()
        
        business = data["business_kpis"]
        assert "cost_optimization_target" in business
        assert "route_accuracy_target" in business
        assert "user_productivity_target" in business
        assert "global_port_coverage" in business
