"""
Database Management
PostgreSQL + asyncpg connection management with connection pooling.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Any, List, Optional

import asyncpg
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class DatabaseManager:
    """
    Async database manager with connection pooling.
    
    Provides efficient database access with:
    - Connection pooling for performance
    - Automatic reconnection handling
    - Query execution with error handling
    """
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or settings.database_url
        # Convert SQLAlchemy URL to asyncpg format
        self.database_url = self.database_url.replace(
            "postgresql+asyncpg://", "postgresql://"
        )
        self._pool: Optional[asyncpg.Pool] = None
        self._connected = False
    
    async def connect(self) -> None:
        """Initialize database connection pool."""
        if self._pool is not None:
            return
        
        try:
            self._pool = await asyncpg.create_pool(
                self.database_url,
                min_size=2,
                max_size=settings.database_pool_size,
                max_inactive_connection_lifetime=300
            )
            self._connected = True
            logger.info("Database connection pool initialized", pool_size=settings.database_pool_size)
        except Exception as e:
            logger.error("Failed to connect to database", error=str(e))
            self._connected = False
            raise
    
    async def disconnect(self) -> None:
        """Close database connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            self._connected = False
            logger.info("Database connection pool closed")
    
    @property
    def is_connected(self) -> bool:
        """Check if database is connected."""
        return self._connected and self._pool is not None
    
    async def execute_query(
        self, 
        query: str, 
        *args,
        timeout: float = 30.0
    ) -> List[asyncpg.Record]:
        """
        Execute a query and return results.
        
        Args:
            query: SQL query string
            *args: Query parameters
            timeout: Query timeout in seconds
            
        Returns:
            List of result records
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self._pool.acquire() as conn:
                result = await conn.fetch(query, *args, timeout=timeout)
                return result
        except asyncpg.PostgresError as e:
            logger.error("Database query failed", query=query[:100], error=str(e))
            raise
    
    async def execute_one(
        self, 
        query: str, 
        *args,
        timeout: float = 30.0
    ) -> Optional[asyncpg.Record]:
        """
        Execute a query and return single result.
        
        Args:
            query: SQL query string
            *args: Query parameters
            timeout: Query timeout in seconds
            
        Returns:
            Single result record or None
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self._pool.acquire() as conn:
                result = await conn.fetchrow(query, *args, timeout=timeout)
                return result
        except asyncpg.PostgresError as e:
            logger.error("Database query failed", query=query[:100], error=str(e))
            raise
    
    async def execute_many(
        self, 
        query: str, 
        args_list: List[tuple],
        timeout: float = 60.0
    ) -> None:
        """
        Execute a query with multiple parameter sets.
        
        Args:
            query: SQL query string
            args_list: List of parameter tuples
            timeout: Query timeout in seconds
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self._pool.acquire() as conn:
                await conn.executemany(query, args_list, timeout=timeout)
        except asyncpg.PostgresError as e:
            logger.error("Database batch query failed", query=query[:100], error=str(e))
            raise
    
    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for database transactions.
        
        Usage:
            async with db.transaction():
                await db.execute_query(...)
        """
        if not self._pool:
            raise RuntimeError("Database not connected")
        
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                yield conn
    
    async def health_check(self) -> bool:
        """Check database connection health."""
        try:
            result = await self.execute_one("SELECT 1 as health")
            return result is not None and result.get("health") == 1
        except Exception as e:
            logger.warning("Database health check failed", error=str(e))
            return False


# Global database manager instance
db_manager = DatabaseManager()
