"""
Maritime Analytics Engine
Comprehensive analytics and business intelligence for maritime route planning.

Features:
- Route calculation performance analytics
- User behavior and engagement tracking
- Cost and efficiency analysis
- Real-time KPI monitoring and reporting
- Trend analysis and forecasting
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from collections import defaultdict
from decimal import Decimal

import structlog

from app.core.database import DatabaseManager
from app.core.cache import CacheService

logger = structlog.get_logger(__name__)


@dataclass
class RouteCalculationMetric:
    """Metrics for a single route calculation."""
    request_id: str
    origin_port: str
    destination_port: str
    calculation_time_ms: float
    routes_found: int
    cache_hit: bool
    algorithm_used: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    primary_route_cost_usd: Optional[float] = None
    primary_route_time_hours: Optional[float] = None
    primary_route_distance_nm: Optional[float] = None


@dataclass
class SystemHealthMetric:
    """System health and performance metrics."""
    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_percent: float
    active_connections: int
    requests_per_minute: int
    average_response_time_ms: float
    error_rate_percent: float


@dataclass
class AnalyticsSummary:
    """Summary of analytics for a time period."""
    period_start: datetime
    period_end: datetime
    total_calculations: int
    successful_calculations: int
    average_calculation_time_ms: float
    cache_hit_ratio: float
    most_popular_routes: List[Dict[str, Any]]
    performance_by_algorithm: Dict[str, Dict[str, float]]
    cost_savings_usd: float


class AnalyticsEngine:
    """
    Enterprise-grade analytics engine for maritime route planning.
    
    Provides comprehensive analytics including:
    - Real-time performance monitoring
    - User behavior analytics
    - Business intelligence dashboards
    - Trend analysis and forecasting
    
    Data retention:
    - Real-time metrics: 24 hours
    - Aggregated metrics: 90 days
    - Historical summaries: Indefinite
    """
    
    def __init__(
        self,
        db_manager: Optional[DatabaseManager] = None,
        cache_service: Optional[CacheService] = None
    ):
        self.db_manager = db_manager
        self.cache_service = cache_service
        
        # In-memory metrics storage (recent data)
        self._route_metrics: List[RouteCalculationMetric] = []
        self._system_metrics: List[SystemHealthMetric] = []
        
        # Aggregated statistics
        self._hourly_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        self._daily_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Route popularity tracking
        self._route_popularity: Dict[str, int] = defaultdict(int)
        
        # KPI tracking
        self._kpis = {
            "target_calculation_time_ms": 500,
            "target_cache_hit_ratio": 0.95,
            "target_success_rate": 0.98
        }
        
        # Max retention for in-memory metrics
        self._max_metrics_retention = 10000
    
    def record_route_calculation(
        self,
        request_id: str,
        origin_port: str,
        destination_port: str,
        calculation_time_ms: float,
        routes_found: int,
        cache_hit: bool,
        algorithm_used: str,
        primary_route_cost_usd: Optional[float] = None,
        primary_route_time_hours: Optional[float] = None,
        primary_route_distance_nm: Optional[float] = None
    ) -> None:
        """
        Record metrics for a route calculation.
        
        Args:
            request_id: Unique request identifier
            origin_port: Origin port code
            destination_port: Destination port code
            calculation_time_ms: Calculation duration in milliseconds
            routes_found: Number of routes found
            cache_hit: Whether result was from cache
            algorithm_used: Pathfinding algorithm used
            primary_route_cost_usd: Cost of primary route
            primary_route_time_hours: Time of primary route
            primary_route_distance_nm: Distance of primary route
        """
        metric = RouteCalculationMetric(
            request_id=request_id,
            origin_port=origin_port,
            destination_port=destination_port,
            calculation_time_ms=calculation_time_ms,
            routes_found=routes_found,
            cache_hit=cache_hit,
            algorithm_used=algorithm_used,
            primary_route_cost_usd=primary_route_cost_usd,
            primary_route_time_hours=primary_route_time_hours,
            primary_route_distance_nm=primary_route_distance_nm
        )
        
        # Store metric
        self._route_metrics.append(metric)
        
        # Update route popularity
        route_key = f"{origin_port}-{destination_port}"
        self._route_popularity[route_key] += 1
        
        # Update hourly aggregations
        hour_key = metric.timestamp.strftime("%Y-%m-%d-%H")
        self._update_hourly_stats(hour_key, metric)
        
        # Prune old metrics if needed
        if len(self._route_metrics) > self._max_metrics_retention:
            self._route_metrics = self._route_metrics[-self._max_metrics_retention // 2:]
        
        logger.debug(
            "Route calculation recorded",
            request_id=request_id,
            calculation_time_ms=calculation_time_ms,
            cache_hit=cache_hit
        )
    
    def record_system_health(
        self,
        cpu_usage: float,
        memory_usage: float,
        active_connections: int,
        requests_per_minute: int,
        average_response_time_ms: float,
        error_rate: float
    ) -> None:
        """
        Record system health metrics.
        
        Args:
            cpu_usage: CPU usage percentage
            memory_usage: Memory usage percentage
            active_connections: Number of active connections
            requests_per_minute: Request rate
            average_response_time_ms: Average response time
            error_rate: Error rate percentage
        """
        metric = SystemHealthMetric(
            timestamp=datetime.utcnow(),
            cpu_usage_percent=cpu_usage,
            memory_usage_percent=memory_usage,
            active_connections=active_connections,
            requests_per_minute=requests_per_minute,
            average_response_time_ms=average_response_time_ms,
            error_rate_percent=error_rate
        )
        
        self._system_metrics.append(metric)
        
        # Prune old metrics
        if len(self._system_metrics) > 1000:
            self._system_metrics = self._system_metrics[-500:]
    
    def get_real_time_metrics(self) -> Dict[str, Any]:
        """
        Get real-time performance metrics.
        
        Returns:
            Dictionary with current performance metrics
        """
        now = datetime.utcnow()
        one_minute_ago = now - timedelta(minutes=1)
        five_minutes_ago = now - timedelta(minutes=5)
        
        # Filter recent metrics
        recent_metrics = [
            m for m in self._route_metrics 
            if m.timestamp > five_minutes_ago
        ]
        
        last_minute_metrics = [
            m for m in recent_metrics 
            if m.timestamp > one_minute_ago
        ]
        
        # Calculate real-time statistics
        if recent_metrics:
            avg_calc_time = sum(m.calculation_time_ms for m in recent_metrics) / len(recent_metrics)
            cache_hits = sum(1 for m in recent_metrics if m.cache_hit)
            cache_hit_ratio = cache_hits / len(recent_metrics)
            success_rate = sum(1 for m in recent_metrics if m.routes_found > 0) / len(recent_metrics)
        else:
            avg_calc_time = 0
            cache_hit_ratio = 0
            success_rate = 0
        
        return {
            "timestamp": now.isoformat(),
            "metrics_period_minutes": 5,
            "total_calculations": len(recent_metrics),
            "calculations_last_minute": len(last_minute_metrics),
            "average_calculation_time_ms": round(avg_calc_time, 2),
            "cache_hit_ratio": round(cache_hit_ratio, 4),
            "success_rate": round(success_rate, 4),
            "kpi_compliance": {
                "calculation_time": avg_calc_time <= self._kpis["target_calculation_time_ms"],
                "cache_hit_ratio": cache_hit_ratio >= self._kpis["target_cache_hit_ratio"],
                "success_rate": success_rate >= self._kpis["target_success_rate"]
            }
        }
    
    def get_analytics_summary(
        self,
        period_hours: int = 24
    ) -> AnalyticsSummary:
        """
        Get analytics summary for a time period.
        
        Args:
            period_hours: Hours to include in summary
            
        Returns:
            AnalyticsSummary with aggregated metrics
        """
        now = datetime.utcnow()
        period_start = now - timedelta(hours=period_hours)
        
        # Filter metrics for period
        period_metrics = [
            m for m in self._route_metrics 
            if m.timestamp > period_start
        ]
        
        if not period_metrics:
            return AnalyticsSummary(
                period_start=period_start,
                period_end=now,
                total_calculations=0,
                successful_calculations=0,
                average_calculation_time_ms=0,
                cache_hit_ratio=0,
                most_popular_routes=[],
                performance_by_algorithm={},
                cost_savings_usd=0
            )
        
        # Calculate aggregated statistics
        total_calculations = len(period_metrics)
        successful = sum(1 for m in period_metrics if m.routes_found > 0)
        avg_calc_time = sum(m.calculation_time_ms for m in period_metrics) / total_calculations
        cache_hits = sum(1 for m in period_metrics if m.cache_hit)
        cache_hit_ratio = cache_hits / total_calculations
        
        # Get most popular routes
        route_counts: Dict[str, int] = defaultdict(int)
        for m in period_metrics:
            route_key = f"{m.origin_port}-{m.destination_port}"
            route_counts[route_key] += 1
        
        most_popular = sorted(
            route_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]
        
        popular_routes = [
            {"route": route, "count": count}
            for route, count in most_popular
        ]
        
        # Performance by algorithm
        algorithm_metrics: Dict[str, List[float]] = defaultdict(list)
        for m in period_metrics:
            algorithm_metrics[m.algorithm_used].append(m.calculation_time_ms)
        
        performance_by_algorithm = {
            algo: {
                "count": len(times),
                "average_time_ms": round(sum(times) / len(times), 2),
                "min_time_ms": round(min(times), 2),
                "max_time_ms": round(max(times), 2)
            }
            for algo, times in algorithm_metrics.items()
        }
        
        # Estimate cost savings (placeholder calculation)
        # Assumes 15% average cost reduction per optimized route
        routes_with_cost = [m for m in period_metrics if m.primary_route_cost_usd]
        if routes_with_cost:
            total_route_cost = sum(m.primary_route_cost_usd for m in routes_with_cost)
            estimated_savings = total_route_cost * 0.15  # 15% savings estimate
        else:
            estimated_savings = 0
        
        return AnalyticsSummary(
            period_start=period_start,
            period_end=now,
            total_calculations=total_calculations,
            successful_calculations=successful,
            average_calculation_time_ms=round(avg_calc_time, 2),
            cache_hit_ratio=round(cache_hit_ratio, 4),
            most_popular_routes=popular_routes,
            performance_by_algorithm=performance_by_algorithm,
            cost_savings_usd=round(estimated_savings, 2)
        )
    
    def get_kpi_report(self) -> Dict[str, Any]:
        """
        Get KPI compliance report.
        
        Returns:
            Dictionary with KPI status and compliance
        """
        real_time = self.get_real_time_metrics()
        summary_24h = self.get_analytics_summary(24)
        summary_7d = self.get_analytics_summary(168)  # 7 days
        
        return {
            "report_timestamp": datetime.utcnow().isoformat(),
            "kpi_targets": self._kpis,
            "real_time_compliance": real_time["kpi_compliance"],
            "performance_24h": {
                "total_calculations": summary_24h.total_calculations,
                "average_calculation_time_ms": summary_24h.average_calculation_time_ms,
                "cache_hit_ratio": summary_24h.cache_hit_ratio,
                "success_rate": summary_24h.successful_calculations / max(summary_24h.total_calculations, 1)
            },
            "performance_7d": {
                "total_calculations": summary_7d.total_calculations,
                "average_calculation_time_ms": summary_7d.average_calculation_time_ms,
                "cache_hit_ratio": summary_7d.cache_hit_ratio,
                "success_rate": summary_7d.successful_calculations / max(summary_7d.total_calculations, 1)
            },
            "trends": self._calculate_trends(),
            "recommendations": self._generate_recommendations(summary_24h)
        }
    
    def _update_hourly_stats(self, hour_key: str, metric: RouteCalculationMetric) -> None:
        """Update hourly aggregated statistics."""
        if hour_key not in self._hourly_stats:
            self._hourly_stats[hour_key] = {
                "count": 0,
                "total_time_ms": 0,
                "cache_hits": 0,
                "successful": 0
            }
        
        stats = self._hourly_stats[hour_key]
        stats["count"] += 1
        stats["total_time_ms"] += metric.calculation_time_ms
        if metric.cache_hit:
            stats["cache_hits"] += 1
        if metric.routes_found > 0:
            stats["successful"] += 1
    
    def _calculate_trends(self) -> Dict[str, str]:
        """Calculate performance trends."""
        # Compare last 12 hours to previous 12 hours
        now = datetime.utcnow()
        recent_cutoff = now - timedelta(hours=12)
        old_cutoff = now - timedelta(hours=24)
        
        recent_metrics = [m for m in self._route_metrics if m.timestamp > recent_cutoff]
        old_metrics = [m for m in self._route_metrics if old_cutoff < m.timestamp <= recent_cutoff]
        
        trends = {}
        
        if recent_metrics and old_metrics:
            recent_avg = sum(m.calculation_time_ms for m in recent_metrics) / len(recent_metrics)
            old_avg = sum(m.calculation_time_ms for m in old_metrics) / len(old_metrics)
            
            if recent_avg < old_avg * 0.95:
                trends["calculation_time"] = "improving"
            elif recent_avg > old_avg * 1.05:
                trends["calculation_time"] = "degrading"
            else:
                trends["calculation_time"] = "stable"
            
            recent_cache = sum(1 for m in recent_metrics if m.cache_hit) / len(recent_metrics)
            old_cache = sum(1 for m in old_metrics if m.cache_hit) / len(old_metrics)
            
            if recent_cache > old_cache + 0.02:
                trends["cache_efficiency"] = "improving"
            elif recent_cache < old_cache - 0.02:
                trends["cache_efficiency"] = "degrading"
            else:
                trends["cache_efficiency"] = "stable"
        else:
            trends["calculation_time"] = "insufficient_data"
            trends["cache_efficiency"] = "insufficient_data"
        
        return trends
    
    def _generate_recommendations(self, summary: AnalyticsSummary) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        if summary.average_calculation_time_ms > self._kpis["target_calculation_time_ms"]:
            recommendations.append(
                "Consider optimizing pathfinding algorithms or increasing cache TTL "
                "to improve calculation times"
            )
        
        if summary.cache_hit_ratio < self._kpis["target_cache_hit_ratio"]:
            recommendations.append(
                "Cache hit ratio is below target. Consider implementing predictive "
                "cache warming for popular routes"
            )
        
        success_rate = summary.successful_calculations / max(summary.total_calculations, 1)
        if success_rate < self._kpis["target_success_rate"]:
            recommendations.append(
                "Success rate is below target. Review error logs and consider "
                "expanding port coverage or improving input validation"
            )
        
        if not recommendations:
            recommendations.append(
                "All KPIs are within target ranges. System is performing optimally."
            )
        
        return recommendations
