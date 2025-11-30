#!/usr/bin/env python
"""
Health Check Script
Check system health and connectivity.
"""

import asyncio
import httpx


async def check_health():
    """Check all system components."""
    print("Checking system health...\n")
    
    checks = {
        "backend": "http://localhost:8000/health",
        "frontend": "http://localhost:5173",
    }
    
    async with httpx.AsyncClient() as client:
        for name, url in checks.items():
            try:
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    print(f"✅ {name}: OK")
                else:
                    print(f"⚠️ {name}: Status {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: Failed ({e})")
    
    print("\nHealth check completed.")


if __name__ == "__main__":
    asyncio.run(check_health())
