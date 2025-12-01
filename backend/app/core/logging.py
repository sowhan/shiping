"""
Structured Logging Configuration
Provides correlation IDs and JSON formatting for production logging.
"""

import logging
import sys
from typing import Any

import structlog
from structlog.types import Processor

from app.core.config import settings


def get_log_level() -> int:
    """Get logging level from settings."""
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return level_map.get(settings.log_level.upper(), logging.INFO)


def setup_logging() -> None:
    """Configure structured logging for the application."""
    
    # Shared processors
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.log_format == "json":
        # JSON formatting for production
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Console formatting for development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=get_log_level(),
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)


def add_correlation_id(correlation_id: str) -> None:
    """Add correlation ID to logging context."""
    structlog.contextvars.bind_contextvars(correlation_id=correlation_id)


def clear_context() -> None:
    """Clear logging context."""
    structlog.contextvars.clear_contextvars()
