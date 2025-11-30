"""
Application Configuration
Environment-based configuration with validation using Pydantic Settings.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = Field(default="Maritime Route Planner", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="development", description="Environment name")
    
    # API Settings
    api_v1_prefix: str = Field(default="/api/v1", description="API version 1 prefix")
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173", 
        description="Allowed CORS origins (comma-separated)"
    )
    
    # Database Settings
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/maritime_routes",
        description="PostgreSQL database connection URL"
    )
    database_pool_size: int = Field(default=10, ge=1, le=50, description="Connection pool size")
    database_max_overflow: int = Field(default=20, ge=0, description="Max overflow connections")
    
    # Redis Cache Settings  
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )
    cache_ttl_seconds: int = Field(default=1800, ge=60, description="Default cache TTL")
    
    # Security Settings
    secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for JWT tokens"
    )
    access_token_expire_minutes: int = Field(default=30, ge=5, description="Access token expiry")
    
    # Performance Settings
    route_calculation_timeout_seconds: int = Field(default=30, ge=5, le=120)
    max_route_alternatives: int = Field(default=5, ge=1, le=10)
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format (json/text)")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()
