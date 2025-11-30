# 🚢 Maritime Route Planning Platform

Enterprise-grade maritime route planning platform that provides intelligent route optimization, real-time analysis, and comprehensive shipping logistics intelligence.

## 🌟 Features

- **Multi-Algorithm Pathfinding**: Dijkstra, A*, and custom maritime heuristics
- **Route Optimization**: Optimize for time, cost, reliability, or balanced approach
- **Global Port Coverage**: 50,000+ ports worldwide
- **Real-time Analysis**: Weather, traffic, and risk factor integration
- **Sub-500ms Performance**: Optimized for production workloads
- **Enterprise Security**: JWT authentication, RBAC, and encryption

## 🏗️ Architecture

```
maritime-route-planner/
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── api/            # REST API endpoints
│   │   ├── core/           # Configuration and database
│   │   ├── models/         # Pydantic data models
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── pages/          # Application pages
│   │   ├── services/       # API services
│   │   ├── store/          # State management
│   │   └── types/          # TypeScript types
│   ├── Dockerfile
│   └── package.json
├── database/               # PostgreSQL + PostGIS schema
│   └── init.sql
├── docker-compose.yml      # Container orchestration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/sowhan/shiping.git
cd shiping

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp ../.env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

## 📡 API Endpoints

### Route Planning

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/routes/calculate` | Calculate optimal maritime routes |
| POST | `/api/v1/routes/validate` | Validate route parameters |

### Port Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/ports/search` | Search ports by name or code |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health status |

## 📊 API Usage Example

```bash
# Calculate route from Singapore to Rotterdam
curl -X POST "http://localhost:8000/api/v1/routes/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_port_code": "SGSIN",
    "destination_port_code": "NLRTM",
    "vessel_constraints": {
      "vessel_type": "container",
      "length_meters": 300,
      "beam_meters": 45,
      "draft_meters": 14,
      "cruise_speed_knots": 18,
      "max_range_nautical_miles": 10000,
      "fuel_type": "vlsfo",
      "suez_canal_compatible": true,
      "panama_canal_compatible": true
    },
    "optimization_criteria": "balanced",
    "include_alternative_routes": true,
    "max_alternative_routes": 3
  }'
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ with PostGIS
- **Cache**: Redis 7+
- **Authentication**: JWT with python-jose

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **State Management**: Zustand
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

### Infrastructure
- **Containers**: Docker & Docker Compose
- **Database**: PostGIS for spatial queries
- **Monitoring**: Structured logging with structlog

## 📈 Performance Targets & KPI Compliance

This application is designed to meet enterprise-grade performance specifications:

### Route Calculations
| Metric | Target | Implementation |
|--------|--------|----------------|
| Simple routes | <500ms (95th percentile) | Multi-algorithm pathfinding with caching |
| Complex multi-hop | <3 seconds (95th percentile) | Hub-based routing optimization |
| Concurrent users | 10,000+ simultaneously | Async architecture with uvloop |
| Cache hit ratio | >95% for repeated requests | Redis with intelligent TTL strategy |

### Database Operations
| Metric | Target | Implementation |
|--------|--------|----------------|
| Port searches | <100ms (99th percentile) | PostGIS indexes + prepared statements |
| Spatial queries | <50ms average | GIST indexes with optimization |
| Connection pool | 10-50 connections | asyncpg with overflow support |

### System Reliability
| Metric | Target | Implementation |
|--------|--------|----------------|
| Uptime SLA | 99.9% | Graceful degradation + health checks |
| Error rate | <2% under peak load | Comprehensive error handling |
| Auto-scaling | 100,000+ daily calculations | Kubernetes-ready containerization |

### Business Impact Goals
| Metric | Target |
|--------|--------|
| Cost optimization | 15-25% average shipping cost reduction |
| Route accuracy | >98% ETA prediction accuracy |
| User productivity | <3 clicks to generate optimal routes |
| Global coverage | 50,000+ ports worldwide |

### Monitoring Endpoints
- `/health` - System health check
- `/metrics` - Real-time KPI tracking and compliance status

## 🔒 Security

- JWT authentication with refresh tokens
- Role-based access control (RBAC)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention
- Rate limiting

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For support, please open an issue on GitHub or contact the development team.
