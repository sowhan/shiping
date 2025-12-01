#!/usr/bin/env python
"""
Production Server Script
Start the backend in production mode with optimization.
"""

import multiprocessing
import uvicorn


def main():
    """Run production server."""
    # Calculate optimal workers based on CPU cores
    workers = multiprocessing.cpu_count() * 2 + 1
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=workers,
        log_level="info",
        access_log=True,
        loop="uvloop",
        http="httptools"
    )


if __name__ == "__main__":
    main()
