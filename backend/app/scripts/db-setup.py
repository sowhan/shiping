#!/usr/bin/env python
"""
Database Setup Script
Initialize database schema and apply migrations.
"""

import asyncio
import asyncpg
from app.core.config import settings


async def setup_database():
    """Initialize database with schema."""
    conn = await asyncpg.connect(settings.database_url.replace("+asyncpg", ""))
    
    # Create PostGIS extension if not exists
    await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    print("Database setup completed successfully")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(setup_database())
