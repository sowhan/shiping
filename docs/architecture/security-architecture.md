# Security Architecture

## Authentication

### JWT Token Flow

```
┌─────────┐      ┌─────────┐      ┌─────────┐
│ Client  │      │ Backend │      │  Redis  │
└────┬────┘      └────┬────┘      └────┬────┘
     │                │                │
     │ POST /auth/login               │
     │───────────────>│                │
     │                │                │
     │  Access Token + Refresh Token  │
     │<───────────────│                │
     │                │                │
     │ GET /api/routes (with token)   │
     │───────────────>│                │
     │                │ Validate JWT   │
     │                │───────────────>│
     │                │<───────────────│
     │    Response    │                │
     │<───────────────│                │
```

### Token Configuration

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"
```

## Role-Based Access Control (RBAC)

### Roles

| Role | Permissions |
|------|-------------|
| viewer | Read routes, ports |
| operator | Create routes, track vessels |
| admin | Full access, user management |
| api_client | Programmatic access |

### Permission Matrix

| Resource | viewer | operator | admin |
|----------|--------|----------|-------|
| GET /routes | ✓ | ✓ | ✓ |
| POST /routes | ✗ | ✓ | ✓ |
| GET /vessels | ✓ | ✓ | ✓ |
| POST /vessels | ✗ | ✓ | ✓ |
| GET /admin/* | ✗ | ✗ | ✓ |

## Encryption

### In Transit
- TLS 1.3 for all API communications
- Certificate management via Let's Encrypt
- HSTS enabled with preloading

### At Rest
- AES-256 for sensitive data
- Database field-level encryption for PII
- Encrypted backups

## Security Headers

```python
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}
```

## Rate Limiting

```python
RATE_LIMITS = {
    "default": "60/minute",
    "auth": "10/minute",
    "search": "100/minute",
    "calculations": "30/minute",
}
```

## Input Validation

- Pydantic models for all API inputs
- SQL injection prevention via parameterized queries
- XSS prevention via output encoding
- Request size limits (10MB max)

## Security Checklist

- [ ] JWT tokens with short expiration
- [ ] Refresh token rotation
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Secure headers enabled
- [ ] Secrets in environment variables
- [ ] Audit logging enabled
