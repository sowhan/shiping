"""
Redis Cache Service
Enterprise Redis caching with intelligent strategy for maritime route planning.
"""

import json
import zlib
import hashlib
from typing import Any, Optional
from datetime import timedelta

import redis.asyncio as redis
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class CacheService:
    """
    Enterprise Redis cache service with compression and intelligent strategies.
    
    Cache TTL Strategy (as per requirements):
    - Route calculations: 30 minutes
    - Port data: 24 hours
    - Vessel positions: 1 minute
    """
    
    # Cache TTL configurations (in seconds)
    TTL_ROUTE_CALCULATIONS = 30 * 60  # 30 minutes
    TTL_PORT_DATA = 24 * 60 * 60  # 24 hours
    TTL_VESSEL_POSITIONS = 60  # 1 minute
    TTL_DEFAULT = settings.cache_ttl_seconds
    
    # Compression threshold (bytes)
    COMPRESSION_THRESHOLD = 1024  # 1KB
    
    def __init__(self):
        self._redis: Optional[redis.Redis] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Initialize Redis connection pool."""
        if self._redis is not None:
            return
        
        try:
            self._redis = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=False,
                max_connections=50
            )
            # Test connection
            await self._redis.ping()
            self._connected = True
            logger.info("Redis connection established", url=settings.redis_url)
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            self._connected = False
            # Don't raise - allow graceful degradation
    
    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None
            self._connected = False
            logger.info("Redis connection closed")
    
    @property
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        return self._connected and self._redis is not None
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key with prefix and hashed identifier."""
        key_hash = hashlib.md5(identifier.encode()).hexdigest()[:12]
        return f"maritime:{prefix}:{key_hash}"
    
    def _compress_value(self, value: bytes) -> bytes:
        """Compress value if it exceeds threshold."""
        if len(value) > self.COMPRESSION_THRESHOLD:
            compressed = zlib.compress(value)
            # Only use compression if it actually reduces size
            if len(compressed) < len(value):
                return b"COMPRESSED:" + compressed
        return value
    
    def _decompress_value(self, value: bytes) -> bytes:
        """Decompress value if it was compressed."""
        if value.startswith(b"COMPRESSED:"):
            return zlib.decompress(value[11:])
        return value
    
    async def get(self, prefix: str, identifier: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            prefix: Cache key prefix (route, port, vessel)
            identifier: Unique identifier
            
        Returns:
            Cached value or None
        """
        if not self.is_connected:
            return None
        
        try:
            key = self._generate_key(prefix, identifier)
            value = await self._redis.get(key)
            
            if value is None:
                return None
            
            decompressed = self._decompress_value(value)
            return json.loads(decompressed.decode())
            
        except Exception as e:
            logger.warning("Cache get failed", key=key, error=str(e))
            return None
    
    async def set(
        self, 
        prefix: str, 
        identifier: str, 
        value: Any, 
        ttl_seconds: Optional[int] = None
    ) -> bool:
        """
        Set value in cache with optional TTL.
        
        Args:
            prefix: Cache key prefix
            identifier: Unique identifier
            value: Value to cache (will be JSON serialized)
            ttl_seconds: TTL in seconds (uses default if not specified)
            
        Returns:
            True if successful
        """
        if not self.is_connected:
            return False
        
        try:
            key = self._generate_key(prefix, identifier)
            serialized = json.dumps(value).encode()
            compressed = self._compress_value(serialized)
            
            ttl = ttl_seconds or self.TTL_DEFAULT
            await self._redis.setex(key, ttl, compressed)
            
            return True
            
        except Exception as e:
            logger.warning("Cache set failed", key=key, error=str(e))
            return False
    
    async def delete(self, prefix: str, identifier: str) -> bool:
        """Delete value from cache."""
        if not self.is_connected:
            return False
        
        try:
            key = self._generate_key(prefix, identifier)
            await self._redis.delete(key)
            return True
        except Exception as e:
            logger.warning("Cache delete failed", key=key, error=str(e))
            return False
    
    # Convenience methods for specific cache types
    
    async def get_route(self, route_key: str) -> Optional[dict]:
        """Get cached route calculation."""
        return await self.get("route", route_key)
    
    async def set_route(self, route_key: str, route_data: dict) -> bool:
        """Cache route calculation with 30-minute TTL."""
        return await self.set("route", route_key, route_data, self.TTL_ROUTE_CALCULATIONS)
    
    async def get_port(self, port_code: str) -> Optional[dict]:
        """Get cached port data."""
        return await self.get("port", port_code)
    
    async def set_port(self, port_code: str, port_data: dict) -> bool:
        """Cache port data with 24-hour TTL."""
        return await self.set("port", port_code, port_data, self.TTL_PORT_DATA)
    
    async def get_vessel_position(self, vessel_id: str) -> Optional[dict]:
        """Get cached vessel position."""
        return await self.get("vessel", vessel_id)
    
    async def set_vessel_position(self, vessel_id: str, position_data: dict) -> bool:
        """Cache vessel position with 1-minute TTL."""
        return await self.set("vessel", vessel_id, position_data, self.TTL_VESSEL_POSITIONS)
    
    async def health_check(self) -> bool:
        """Check Redis connection health."""
        if not self.is_connected:
            return False
        try:
            await self._redis.ping()
            return True
        except Exception:
            return False


# Global cache service instance
cache_service = CacheService()
