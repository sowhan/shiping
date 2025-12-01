# Kubernetes Deployment

## Overview

Deploy the Maritime Route Planning Platform to Kubernetes for production-grade scalability and reliability.

## Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Helm 3.x (optional)
- Container registry access

## Quick Start

```bash
# Apply all manifests
kubectl apply -f infrastructure/kubernetes/

# Verify deployment
kubectl get pods -n maritime

# Check services
kubectl get svc -n maritime
```

## Manifests

### Namespace

```yaml
# infrastructure/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: maritime
  labels:
    app: maritime-routes
```

### ConfigMap

```yaml
# infrastructure/kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: maritime-config
  namespace: maritime
data:
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"
  API_PREFIX: "/api/v1"
```

### Backend Deployment

```yaml
# infrastructure/kubernetes/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: maritime-backend
  namespace: maritime
spec:
  replicas: 3
  selector:
    matchLabels:
      app: maritime-backend
  template:
    metadata:
      labels:
        app: maritime-backend
    spec:
      containers:
      - name: backend
        image: maritime-routes/backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: maritime-config
        - secretRef:
            name: maritime-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Frontend Deployment

```yaml
# infrastructure/kubernetes/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: maritime-frontend
  namespace: maritime
spec:
  replicas: 2
  selector:
    matchLabels:
      app: maritime-frontend
  template:
    metadata:
      labels:
        app: maritime-frontend
    spec:
      containers:
      - name: frontend
        image: maritime-routes/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

### Services

```yaml
# infrastructure/kubernetes/services.yaml
apiVersion: v1
kind: Service
metadata:
  name: maritime-backend
  namespace: maritime
spec:
  selector:
    app: maritime-backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
---
apiVersion: v1
kind: Service
metadata:
  name: maritime-frontend
  namespace: maritime
spec:
  selector:
    app: maritime-frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

### Ingress

```yaml
# infrastructure/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: maritime-ingress
  namespace: maritime
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - api.maritime-routes.com
    secretName: maritime-tls
  rules:
  - host: api.maritime-routes.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: maritime-backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: maritime-frontend
            port:
              number: 80
```

### Horizontal Pod Autoscaler

```yaml
# infrastructure/kubernetes/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: maritime-backend-hpa
  namespace: maritime
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: maritime-backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Monitoring

```bash
# View pods
kubectl get pods -n maritime

# View logs
kubectl logs -f deployment/maritime-backend -n maritime

# Check HPA status
kubectl get hpa -n maritime

# Port forward for debugging
kubectl port-forward svc/maritime-backend 8000:8000 -n maritime
```

## Scaling

```bash
# Manual scaling
kubectl scale deployment maritime-backend --replicas=5 -n maritime

# Check scaling events
kubectl describe hpa maritime-backend-hpa -n maritime
```
