"""
Rate Limiting Middleware
Enterprise rate limiting with multiple strategies for API protection.
"""

import time
from typing import Dict, Optional, Callable
from collections import defaultdict
import asyncio

from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter with configurable limits.
    
    Features:
    - Per-IP rate limiting
    - Per-user rate limiting
    - Configurable limits per endpoint
    - Sliding window algorithm
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_limit: int = 10
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.burst_limit = burst_limit
        
        # Storage for rate limiting data
        self._minute_counts: Dict[str, list] = defaultdict(list)
        self._hour_counts: Dict[str, list] = defaultdict(list)
        self._last_cleanup = time.time()
    
    def _cleanup_old_requests(self, key: str) -> None:
        """Remove expired request timestamps."""
        current_time = time.time()
        
        # Clean minute window
        minute_ago = current_time - 60
        self._minute_counts[key] = [
            t for t in self._minute_counts[key] if t > minute_ago
        ]
        
        # Clean hour window
        hour_ago = current_time - 3600
        self._hour_counts[key] = [
            t for t in self._hour_counts[key] if t > hour_ago
        ]
    
    def _get_client_key(self, request: Request) -> str:
        """Get unique client identifier from request."""
        # Try to get user ID from authenticated user
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"
        
        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        return f"ip:{client_ip}"
    
    def check_rate_limit(self, request: Request) -> tuple[bool, Dict[str, int]]:
        """
        Check if request is within rate limits.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        client_key = self._get_client_key(request)
        current_time = time.time()
        
        # Cleanup old requests periodically
        if current_time - self._last_cleanup > 60:
            self._cleanup_old_requests(client_key)
            self._last_cleanup = current_time
        
        # Check minute limit
        minute_count = len([
            t for t in self._minute_counts[client_key] 
            if t > current_time - 60
        ])
        
        # Check hour limit
        hour_count = len([
            t for t in self._hour_counts[client_key] 
            if t > current_time - 3600
        ])
        
        # Check burst (last 5 seconds)
        burst_count = len([
            t for t in self._minute_counts[client_key] 
            if t > current_time - 5
        ])
        
        rate_info = {
            "X-RateLimit-Limit-Minute": self.requests_per_minute,
            "X-RateLimit-Remaining-Minute": max(0, self.requests_per_minute - minute_count),
            "X-RateLimit-Limit-Hour": self.requests_per_hour,
            "X-RateLimit-Remaining-Hour": max(0, self.requests_per_hour - hour_count),
        }
        
        # Check limits
        if burst_count >= self.burst_limit:
            logger.warning("Burst limit exceeded", client=client_key, count=burst_count)
            return False, rate_info
        
        if minute_count >= self.requests_per_minute:
            logger.warning("Minute limit exceeded", client=client_key, count=minute_count)
            return False, rate_info
        
        if hour_count >= self.requests_per_hour:
            logger.warning("Hour limit exceeded", client=client_key, count=hour_count)
            return False, rate_info
        
        # Record this request
        self._minute_counts[client_key].append(current_time)
        self._hour_counts[client_key].append(current_time)
        
        return True, rate_info


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting.
    
    Applies rate limiting to all API endpoints with configurable limits.
    """
    
    # Endpoints exempt from rate limiting
    EXEMPT_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        burst_limit: int = 10
    ):
        super().__init__(app)
        self.rate_limiter = RateLimiter(
            requests_per_minute=requests_per_minute,
            requests_per_hour=requests_per_hour,
            burst_limit=burst_limit
        )
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and apply rate limiting."""
        
        # Skip rate limiting for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)
        
        # Check rate limit
        is_allowed, rate_info = self.rate_limiter.check_rate_limit(request)
        
        if not is_allowed:
            # Return 429 Too Many Requests
            response = Response(
                content='{"error": "Rate limit exceeded", "message": "Too many requests. Please try again later."}',
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                media_type="application/json"
            )
            # Add rate limit headers
            for header, value in rate_info.items():
                response.headers[header] = str(value)
            response.headers["Retry-After"] = "60"
            return response
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        for header, value in rate_info.items():
            response.headers[header] = str(value)
        
        return response


# Convenience function for creating rate limit middleware
def create_rate_limiter(
    requests_per_minute: int = 60,
    requests_per_hour: int = 1000,
    burst_limit: int = 10
) -> RateLimitMiddleware:
    """
    Create rate limiter middleware with custom limits.
    
    Args:
        requests_per_minute: Max requests per minute per client
        requests_per_hour: Max requests per hour per client
        burst_limit: Max requests in a 5-second burst
        
    Returns:
        Configured RateLimitMiddleware
    """
    return lambda app: RateLimitMiddleware(
        app,
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour,
        burst_limit=burst_limit
    )
