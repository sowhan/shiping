# Security Hardening Guide

## Production Security Checklist

### Application Layer

- [ ] JWT tokens with short expiration (30 minutes)
- [ ] Refresh token rotation
- [ ] Password hashing with bcrypt (cost factor 12+)
- [ ] Input validation on all endpoints
- [ ] Output encoding to prevent XSS
- [ ] CSRF protection for state-changing operations
- [ ] SQL injection prevention via parameterized queries
- [ ] File upload restrictions and scanning

### Network Layer

- [ ] TLS 1.3 for all communications
- [ ] HSTS with preloading
- [ ] Certificate pinning for mobile apps
- [ ] WAF configured with OWASP rules
- [ ] DDoS protection enabled
- [ ] VPN for administrative access

### Infrastructure Layer

- [ ] Private subnets for databases
- [ ] Security groups with minimal access
- [ ] Network ACLs configured
- [ ] Bastion host for SSH access
- [ ] No root access on containers
- [ ] Read-only file systems where possible

### Data Layer

- [ ] Encryption at rest (AES-256)
- [ ] Database encryption enabled
- [ ] Backup encryption
- [ ] PII masking in logs
- [ ] Data retention policies

## Security Headers

```nginx
# nginx.conf security headers
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options DENY always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.mapbox.com wss:; frame-ancestors 'none';" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

## Secrets Management

### Environment Variables

```bash
# Never commit secrets to version control
# Use environment variables or secret managers

# Development (.env - gitignored)
SECRET_KEY=dev-only-secret-key
DATABASE_PASSWORD=dev-password

# Production (use AWS Secrets Manager, Vault, etc.)
aws secretsmanager get-secret-value --secret-id maritime/production
```

### Kubernetes Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: maritime-secrets
  namespace: maritime
type: Opaque
data:
  SECRET_KEY: <base64-encoded-secret>
  DATABASE_PASSWORD: <base64-encoded-password>
```

## Rate Limiting

```python
# Rate limiting configuration
RATE_LIMITS = {
    "default": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000,
        "burst": 10
    },
    "auth": {
        "requests_per_minute": 10,
        "requests_per_hour": 50,
        "lockout_duration": 900  # 15 minutes
    },
    "routes/calculate": {
        "requests_per_minute": 30,
        "requests_per_hour": 300
    }
}
```

## Audit Logging

```python
# Log all security-relevant events
audit_events = [
    "user.login",
    "user.logout",
    "user.password_change",
    "admin.user_create",
    "admin.user_delete",
    "api.rate_limit_exceeded",
    "api.authentication_failed"
]

def log_audit_event(event_type, user_id, details):
    logger.info(
        "AUDIT",
        event_type=event_type,
        user_id=user_id,
        ip_address=get_client_ip(),
        timestamp=datetime.utcnow().isoformat(),
        details=details
    )
```

## Vulnerability Scanning

### Dependency Scanning

```bash
# Python dependencies
pip-audit

# Node.js dependencies
npm audit

# Container images
trivy image maritime-routes/backend:latest
```

### SAST (Static Analysis)

```bash
# Python
bandit -r backend/app/

# TypeScript
eslint --ext .ts,.tsx frontend/src/ --rule 'security/detect-*:error'
```

## Incident Response

### Response Procedures

1. **Detection** - Monitor alerts and logs
2. **Containment** - Isolate affected systems
3. **Eradication** - Remove threat
4. **Recovery** - Restore services
5. **Lessons Learned** - Post-incident review

### Emergency Contacts

- Security Team: security@example.com
- On-call Engineer: PagerDuty
- Management Escalation: As per runbook

## Compliance

### GDPR Considerations

- Data minimization
- Right to erasure (data deletion)
- Data portability
- Privacy by design
- Consent management

### SOC 2 Controls

- Access control policies
- Change management
- Incident response
- Business continuity
- Vendor management
