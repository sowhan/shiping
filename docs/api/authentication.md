# Authentication API

## Overview

The Maritime Route Planning Platform uses JWT (JSON Web Tokens) for authentication with refresh token support.

## Token Types

| Token Type | Expiration | Purpose |
|------------|------------|---------|
| Access Token | 30 minutes | API authentication |
| Refresh Token | 7 days | Obtain new access token |

## Endpoints

### POST /api/v1/auth/login

Authenticate user and get tokens.

**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "role": "operator"
  }
}
```

### POST /api/v1/auth/refresh

Get new access token using refresh token.

**Request:**
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

### POST /api/v1/auth/logout

Invalidate tokens.

**Request:**
```http
POST /api/v1/auth/logout
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### POST /api/v1/auth/register

Register new user (admin only).

**Request:**
```http
POST /api/v1/auth/register
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "email": "newuser@example.com",
  "password": "secure_password",
  "role": "operator",
  "name": "John Doe"
}
```

## Using Tokens

Include the access token in the Authorization header:

```http
GET /api/v1/routes/calculate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Role-Based Access Control

| Role | Permissions |
|------|-------------|
| viewer | Read routes, ports |
| operator | Create routes, track vessels |
| admin | Full access |
| api_client | Programmatic API access |

## Token Payload

```json
{
  "sub": "user_123",
  "email": "user@example.com",
  "role": "operator",
  "exp": 1705312800,
  "iat": 1705311000
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "AUTHENTICATION_REQUIRED",
  "message": "Valid authentication credentials required"
}
```

### 403 Forbidden
```json
{
  "error": "INSUFFICIENT_PERMISSIONS",
  "message": "Your role does not have permission for this action"
}
```

## Security Best Practices

1. **Store tokens securely** - Use httpOnly cookies or secure storage
2. **Refresh proactively** - Refresh tokens before expiration
3. **Logout on all devices** - Invalidate all tokens on security events
4. **Use HTTPS** - Never transmit tokens over unencrypted connections
