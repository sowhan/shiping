"""
Route Calculator Worker
Background tasks for complex route calculations.
"""

from typing import Any

from app.workers import celery_app
from app.services.route_planner import MaritimeRoutePlanner
import structlog

logger = structlog.get_logger(__name__)


@celery_app.task(bind=True, max_retries=3)
def calculate_complex_route(
    self,
    origin_port: str,
    destination_port: str,
    vessel_constraints: dict[str, Any],
    optimization_criteria: str
) -> dict[str, Any]:
    """
    Calculate complex route in background.
    
    Used for routes that may take longer than the API timeout.
    """
    try:
        logger.info(
            "Starting background route calculation",
            task_id=self.request.id,
            origin=origin_port,
            destination=destination_port
        )
        
        # Initialize planner
        planner = MaritimeRoutePlanner()
        
        # Calculate route
        result = planner.calculate_route(
            origin_port=origin_port,
            destination_port=destination_port,
            vessel_constraints=vessel_constraints,
            optimization_criteria=optimization_criteria
        )
        
        logger.info(
            "Background route calculation completed",
            task_id=self.request.id,
            success=True
        )
        
        return result
        
    except Exception as exc:
        logger.error(
            "Background route calculation failed",
            task_id=self.request.id,
            error=str(exc)
        )
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@celery_app.task
def warm_route_cache(routes: list[dict[str, str]]) -> dict[str, Any]:
    """
    Pre-calculate and cache popular routes.
    
    Called periodically to maintain cache warmth.
    """
    results = {
        "total": len(routes),
        "successful": 0,
        "failed": 0
    }
    
    planner = MaritimeRoutePlanner()
    
    for route in routes:
        try:
            planner.calculate_route(
                origin_port=route["origin"],
                destination_port=route["destination"],
                vessel_constraints=route.get("vessel_constraints", {}),
                optimization_criteria=route.get("optimization", "balanced")
            )
            results["successful"] += 1
        except Exception as e:
            logger.warning(
                "Cache warming failed for route",
                origin=route["origin"],
                destination=route["destination"],
                error=str(e)
            )
            results["failed"] += 1
    
    return results
