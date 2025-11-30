"""
Maritime Route Planning API
Production-grade FastAPI application with comprehensive route planning features.
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog

from app.core.config import settings
from app.core.database import DatabaseManager
from app.core.cache import cache_service
from app.core.rate_limiter import RateLimitMiddleware
from app.services.route_planner import MaritimeRoutePlanner
from app.api.routes import router as routes_router

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for database connections,
    Redis cache, and service initialization.
    """
    startup_time = datetime.utcnow()
    
    # Initialize database connection
    logger.info("🚀 Starting Maritime Route Planner API", 
                version=settings.app_version,
                environment=settings.environment)
    
    try:
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.connect()
        app.state.db_manager = db_manager
        
        # Initialize Redis cache
        await cache_service.connect()
        app.state.cache_service = cache_service
        
        # Initialize route planner service with cache
        route_planner = MaritimeRoutePlanner(db_manager, cache_service)
        app.state.route_planner = route_planner
        
        # Store startup time for uptime calculation
        app.state.startup_time = startup_time
        
        logger.info("✅ Application startup complete",
                   database_connected=db_manager.is_connected,
                   cache_connected=cache_service.is_connected)
    except Exception as e:
        logger.error("❌ Startup failed", error=str(e))
        # Continue without database for health check availability
        app.state.db_manager = None
        app.state.cache_service = None
        app.state.route_planner = None
        app.state.startup_time = startup_time
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Maritime Route Planner API")
    if hasattr(app.state, 'db_manager') and app.state.db_manager:
        await app.state.db_manager.disconnect()
    if hasattr(app.state, 'cache_service') and app.state.cache_service:
        await app.state.cache_service.disconnect()
    logger.info("✅ Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="""
    ## Maritime Route Planning API
    
    Enterprise-grade route planning service for global shipping operations.
    
    ### Features:
    - **Multi-algorithm pathfinding**: Dijkstra, A*, and custom maritime algorithms
    - **Real-time optimization**: Weather, traffic, and cost factors
    - **Global port coverage**: 50,000+ ports worldwide
    - **Sub-500ms performance**: Optimized for production workloads
    - **JWT Authentication**: Secure access with role-based permissions
    - **Rate Limiting**: Protection against API abuse
    
    ### Endpoints:
    - `/api/v1/routes/calculate` - Calculate optimal maritime routes
    - `/api/v1/routes/validate` - Validate route parameters
    - `/api/v1/ports/search` - Search maritime ports
    - `/api/v1/auth/login` - Authenticate and get tokens
    - `/health` - System health check
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add Rate Limiting Middleware
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60,
    requests_per_hour=1000,
    burst_limit=10
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    routes_router,
    prefix=settings.api_v1_prefix,
    tags=["Route Planning"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    """
    System health check endpoint.
    
    Returns:
        Health status with database, cache, and service connectivity
    """
    uptime = 0.0
    if hasattr(app.state, 'startup_time') and app.state.startup_time:
        uptime = (datetime.utcnow() - app.state.startup_time).total_seconds()
    
    db_connected = False
    if hasattr(app.state, 'db_manager') and app.state.db_manager:
        try:
            db_connected = await app.state.db_manager.health_check()
        except Exception:
            pass
    
    cache_connected = False
    if hasattr(app.state, 'cache_service') and app.state.cache_service:
        try:
            cache_connected = await app.state.cache_service.health_check()
        except Exception:
            pass
    
    status = "healthy"
    if not db_connected:
        status = "degraded"
    if not cache_connected:
        status = "degraded" if status == "healthy" else status
    
    return {
        "status": status,
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat(),
        "uptime_seconds": round(uptime, 2),
        "database_connected": db_connected,
        "cache_connected": cache_connected
    }


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with service information."""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "documentation": "/docs",
        "health": "/health"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unhandled exceptions with structured logging."""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=str(request.url.path),
        method=request.method
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
