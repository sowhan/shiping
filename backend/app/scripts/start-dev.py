#!/usr/bin/env python
"""
Development Server Script
Start the backend in development mode with hot reload.
"""

import uvicorn


def main():
    """Run development server."""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        access_log=True
    )


if __name__ == "__main__":
    main()
