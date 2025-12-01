"""
Authentication & Authorization Service
JWT authentication with refresh tokens and role-based access control (RBAC).
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Security bearer
security = HTTPBearer(auto_error=False)


class UserRole(str, Enum):
    """User roles for RBAC."""
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
    API_USER = "api_user"


class TokenType(str, Enum):
    """Token types."""
    ACCESS = "access"
    REFRESH = "refresh"


class TokenData(BaseModel):
    """Token payload data."""
    user_id: str
    username: str
    role: UserRole
    token_type: TokenType
    exp: datetime


class User(BaseModel):
    """User model."""
    id: str
    username: str
    email: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthService:
    """
    Authentication service with JWT tokens and RBAC.
    
    Features:
    - Password hashing with bcrypt
    - JWT access and refresh tokens
    - Role-based access control
    - Token refresh mechanism
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_token(
        user_id: str,
        username: str,
        role: UserRole,
        token_type: TokenType,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT token.
        
        Args:
            user_id: User's unique identifier
            username: User's username
            role: User's role for RBAC
            token_type: Type of token (access or refresh)
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT token
        """
        if expires_delta is None:
            if token_type == TokenType.ACCESS:
                expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            else:
                expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "sub": user_id,
            "username": username,
            "role": role.value,
            "type": token_type.value,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    
    @staticmethod
    def create_tokens(user: User) -> TokenResponse:
        """
        Create access and refresh token pair.
        
        Args:
            user: User object
            
        Returns:
            TokenResponse with both tokens
        """
        access_token = AuthService.create_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
            token_type=TokenType.ACCESS
        )
        
        refresh_token = AuthService.create_token(
            user_id=user.id,
            username=user.username,
            role=user.role,
            token_type=TokenType.REFRESH
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def decode_token(token: str) -> Optional[TokenData]:
        """
        Decode and validate a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            TokenData if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
            
            return TokenData(
                user_id=payload.get("sub"),
                username=payload.get("username"),
                role=UserRole(payload.get("role")),
                token_type=TokenType(payload.get("type")),
                exp=datetime.fromtimestamp(payload.get("exp"))
            )
            
        except JWTError as e:
            logger.warning("Token decode failed", error=str(e))
            return None
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> Optional[str]:
        """
        Create new access token from refresh token.
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token or None if invalid
        """
        token_data = AuthService.decode_token(refresh_token)
        
        if token_data is None:
            return None
        
        if token_data.token_type != TokenType.REFRESH:
            return None
        
        if token_data.exp < datetime.utcnow():
            return None
        
        return AuthService.create_token(
            user_id=token_data.user_id,
            username=token_data.username,
            role=token_data.role,
            token_type=TokenType.ACCESS
        )


# Dependency functions for FastAPI

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[TokenData]:
    """
    Get current user from token (optional).
    Returns None if no valid token provided.
    """
    if credentials is None:
        return None
    
    token_data = AuthService.decode_token(credentials.credentials)
    
    if token_data is None:
        return None
    
    if token_data.token_type != TokenType.ACCESS:
        return None
    
    if token_data.exp < datetime.utcnow():
        return None
    
    return token_data


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> TokenData:
    """
    Get current user from token (required).
    Raises HTTPException if no valid token.
    """
    user = await get_current_user_optional(credentials)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user


def require_role(*allowed_roles: UserRole):
    """
    Dependency factory for role-based access control.
    
    Usage:
        @router.get("/admin")
        async def admin_only(user: TokenData = Depends(require_role(UserRole.ADMIN))):
            ...
    """
    async def role_checker(
        user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {[r.value for r in allowed_roles]}"
            )
        return user
    
    return role_checker


# Export authentication service instance
auth_service = AuthService()
