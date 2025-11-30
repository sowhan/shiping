"""
Custom Exception Classes
Application-specific exceptions with error codes.
"""

from typing import Any, Optional


class MaritimeBaseException(Exception):
    """Base exception for maritime application."""
    
    error_code: str = "MARITIME_ERROR"
    status_code: int = 500
    
    def __init__(
        self,
        message: str,
        details: Optional[dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.details = details or {}
        if error_code:
            self.error_code = error_code
        super().__init__(self.message)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API response."""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }


class ValidationError(MaritimeBaseException):
    """Validation error for invalid input."""
    error_code = "VALIDATION_ERROR"
    status_code = 400


class AuthenticationError(MaritimeBaseException):
    """Authentication failed."""
    error_code = "AUTHENTICATION_FAILED"
    status_code = 401


class AuthorizationError(MaritimeBaseException):
    """Authorization denied."""
    error_code = "AUTHORIZATION_DENIED"
    status_code = 403


class ResourceNotFoundError(MaritimeBaseException):
    """Resource not found."""
    error_code = "RESOURCE_NOT_FOUND"
    status_code = 404


class RateLimitExceededError(MaritimeBaseException):
    """Rate limit exceeded."""
    error_code = "RATE_LIMIT_EXCEEDED"
    status_code = 429


class RouteCalculationError(MaritimeBaseException):
    """Route calculation failed."""
    error_code = "ROUTE_CALCULATION_ERROR"
    status_code = 500


class RouteNotFoundError(MaritimeBaseException):
    """No valid route found."""
    error_code = "ROUTE_NOT_FOUND"
    status_code = 404


class CalculationTimeoutError(MaritimeBaseException):
    """Route calculation timed out."""
    error_code = "CALCULATION_TIMEOUT"
    status_code = 408


class PortNotFoundError(MaritimeBaseException):
    """Port not found in database."""
    error_code = "PORT_NOT_FOUND"
    status_code = 404


class VesselConstraintError(MaritimeBaseException):
    """Vessel constraints incompatible with route."""
    error_code = "VESSEL_CONSTRAINT_ERROR"
    status_code = 400


class DatabaseError(MaritimeBaseException):
    """Database operation failed."""
    error_code = "DATABASE_ERROR"
    status_code = 500


class CacheError(MaritimeBaseException):
    """Cache operation failed."""
    error_code = "CACHE_ERROR"
    status_code = 500


class ExternalServiceError(MaritimeBaseException):
    """External service integration failed."""
    error_code = "EXTERNAL_SERVICE_ERROR"
    status_code = 502
