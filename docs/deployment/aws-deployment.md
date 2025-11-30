# AWS Deployment Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                                │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                        VPC                                   ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ ││
│  │  │ Route 53    │  │ CloudFront  │  │ WAF                 │ ││
│  │  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘ ││
│  │         │                │                    │             ││
│  │         └────────────────┴────────────────────┘             ││
│  │                          │                                   ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │                  Application Load Balancer              │││
│  │  └─────────────────────────┬───────────────────────────────┘││
│  │                            │                                 ││
│  │  ┌─────────────────────────┴───────────────────────────────┐││
│  │  │                     EKS Cluster                          │││
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │││
│  │  │  │  Backend    │  │  Frontend   │  │  Workers        │ │││
│  │  │  │  Pods       │  │  Pods       │  │  Pods           │ │││
│  │  │  └─────────────┘  └─────────────┘  └─────────────────┘ │││
│  │  └──────────────────────────────────────────────────────────┘││
│  │                            │                                 ││
│  │  ┌─────────────────────────┴───────────────────────────────┐││
│  │  │                    Data Layer                            │││
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │││
│  │  │  │ RDS         │  │ ElastiCache │  │ S3              │ │││
│  │  │  │ PostgreSQL  │  │ Redis       │  │ Storage         │ │││
│  │  │  └─────────────┘  └─────────────┘  └─────────────────┘ │││
│  │  └──────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Terraform 1.5+ (for infrastructure)
- kubectl configured for EKS

## Infrastructure Setup

### Terraform Configuration

```hcl
# infrastructure/terraform/main.tf
provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  
  name = "maritime-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = false
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "maritime-cluster"
  cluster_version = "1.28"
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    general = {
      min_size     = 2
      max_size     = 10
      desired_size = 3
      
      instance_types = ["t3.medium"]
    }
  }
}

module "rds" {
  source = "terraform-aws-modules/rds/aws"
  
  identifier = "maritime-db"
  
  engine            = "postgres"
  engine_version    = "15.4"
  instance_class    = "db.t3.medium"
  allocated_storage = 100
  
  db_name  = "maritime_routes"
  username = "maritime_user"
  port     = "5432"
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  subnet_ids             = module.vpc.private_subnets
  
  multi_az = true
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "maritime-redis"
  engine               = "redis"
  node_type            = "cache.t3.medium"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  
  subnet_group_name = aws_elasticache_subnet_group.redis.name
}
```

## Deployment Steps

### 1. Infrastructure Provisioning

```bash
# Initialize Terraform
cd infrastructure/terraform
terraform init

# Plan infrastructure
terraform plan -out=tfplan

# Apply infrastructure
terraform apply tfplan
```

### 2. EKS Configuration

```bash
# Update kubeconfig
aws eks update-kubeconfig --name maritime-cluster --region us-east-1

# Verify cluster access
kubectl get nodes
```

### 3. Application Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f infrastructure/kubernetes/

# Verify deployment
kubectl get pods -n maritime
```

### 4. DNS and SSL

```bash
# Create Route 53 record pointing to ALB
# Configure ACM certificate for SSL
```

## Cost Optimization

| Service | Configuration | Monthly Cost (est.) |
|---------|--------------|---------------------|
| EKS | 3 t3.medium nodes | ~$150 |
| RDS | db.t3.medium multi-AZ | ~$100 |
| ElastiCache | cache.t3.medium | ~$50 |
| ALB | Application Load Balancer | ~$25 |
| Data Transfer | ~100GB/month | ~$10 |
| **Total** | | **~$335/month** |

## Monitoring

- **CloudWatch** for metrics and logs
- **X-Ray** for distributed tracing
- **CloudWatch Alarms** for alerting

## Security Best Practices

- VPC with private subnets for databases
- Security groups with minimal access
- Secrets in AWS Secrets Manager
- IAM roles for service accounts
- WAF for API protection
