"""
Performance monitoring utilities.
Decorators and helpers for monitoring API and service performance.
"""

import asyncio
import functools
import time
from typing import Callable, Any

import structlog

logger = structlog.get_logger(__name__)


def performance_monitor(operation_name: str):
    """
    Decorator to monitor async function performance.
    
    Args:
        operation_name: Name of the operation for logging
        
    Returns:
        Decorated function with performance monitoring
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                
                logger.info(
                    f"Performance: {operation_name}",
                    operation=operation_name,
                    duration_ms=round(duration_ms, 2),
                    status="success"
                )
                
                return result
                
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                
                logger.warning(
                    f"Performance: {operation_name}",
                    operation=operation_name,
                    duration_ms=round(duration_ms, 2),
                    status="error",
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator


def sync_performance_monitor(operation_name: str):
    """
    Decorator to monitor sync function performance.
    
    Args:
        operation_name: Name of the operation for logging
        
    Returns:
        Decorated function with performance monitoring
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                duration_ms = (time.perf_counter() - start_time) * 1000
                
                logger.info(
                    f"Performance: {operation_name}",
                    operation=operation_name,
                    duration_ms=round(duration_ms, 2),
                    status="success"
                )
                
                return result
                
            except Exception as e:
                duration_ms = (time.perf_counter() - start_time) * 1000
                
                logger.warning(
                    f"Performance: {operation_name}",
                    operation=operation_name,
                    duration_ms=round(duration_ms, 2),
                    status="error",
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator


class PerformanceTracker:
    """
    Context manager for tracking operation performance.
    
    Usage:
        async with PerformanceTracker("route_calculation") as tracker:
            result = await calculate_route(...)
        # Duration automatically logged
    """
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time: float = 0
        self.duration_ms: float = 0
    
    async def __aenter__(self):
        self.start_time = time.perf_counter()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.duration_ms = (time.perf_counter() - self.start_time) * 1000
        
        status = "success" if exc_type is None else "error"
        logger.info(
            f"Performance: {self.operation_name}",
            operation=self.operation_name,
            duration_ms=round(self.duration_ms, 2),
            status=status
        )
        
        return False  # Don't suppress exceptions
