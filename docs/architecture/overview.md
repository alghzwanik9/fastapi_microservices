# Microservices Architecture Documentation

## Overview

This project implements a microservices architecture using FastAPI, PostgreSQL, RabbitMQ, Docker, and Kubernetes.

## Services

### 1. User Service
- **Port**: 8001 (Docker), 8000 (internal)
- **Responsibilities**: User authentication, registration, profile management
- **Database**: PostgreSQL (users_db)
- **Endpoints**:
  - `POST /api/v1/users/register` - Register new user
  - `POST /api/v1/users/login` - User login
  - `GET /api/v1/users/me` - Get current user
  - `GET /api/v1/users/{id}` - Get user by ID
  - `PUT /api/v1/users/{id}` - Update user
  - `DELETE /api/v1/users/{id}` - Delete user

### 2. Product Service (Placeholder)
- **Port**: 8002 (Docker), 8000 (internal)
- **Responsibilities**: Product catalog management

### 3. Order Service (Placeholder)
- **Port**: 8003 (Docker), 8000 (internal)
- **Responsibilities**: Order processing and management

## Communication Pattern

### Synchronous
- REST API calls between services (when needed)
- API Gateway routing

### Asynchronous
- RabbitMQ for event-driven communication
- Topics:
  - `user.created` - Published when new user registers
  - `user.updated` - Published when user profile changes
  - `order.created` - Published when new order is placed

## Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL 15 |
| Message Broker | RabbitMQ 3 |
| Containerization | Docker |
| Orchestration | Kubernetes |
| API Gateway | Nginx |

## Project Structure

```
root/
├── docs/                    # Documentation
│   ├── architecture/        # Architecture diagrams and decisions
│   ├── api/                 # API documentation
│   └── user_manual/         # User guides
├── services/
│   ├── user_service/        # User management service
│   ├── product_service/     # Product catalog service
│   ├── order_service/       # Order processing service
│   └── common/              # Shared utilities and libraries
├── docker/                  # Docker configurations
│   ├── docker-compose.yml   # Local development setup
│   ├── Dockerfile.*         # Service-specific Dockerfiles
│   └── nginx.conf           # API Gateway configuration
├── k8s/                     # Kubernetes manifests
│   ├── deployments/         # Deployment configurations
│   ├── services/            # Service definitions
│   └── ingress/             # Ingress rules
└── tests/                   # Test suites
    ├── functional/          # Functional tests
    └── performance/         # Performance tests
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Poetry (for dependency management)

### Local Development

1. **Start all services with Docker Compose**:
```bash
cd docker
docker-compose up -d
```

2. **Access services**:
- User Service API: http://localhost:8001
- Product Service API: http://localhost:8002
- Order Service API: http://localhost:8003
- API Gateway: http://localhost:80
- RabbitMQ Management: http://localhost:15672
- PostgreSQL: localhost:5432

3. **Run tests**:
```bash
cd tests
pytest functional/
```

### Kubernetes Deployment

1. **Build and push images**:
```bash
docker build -t microservices/user-service:latest -f docker/Dockerfile.user_service .
docker push microservices/user-service:latest
```

2. **Apply Kubernetes manifests**:
```bash
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress/
```

3. **Create secrets**:
```bash
kubectl create secret generic db-secret --from-literal=url='postgresql://user:pass@host:5432/db'
kubectl create secret generic jwt-secret --from-literal=key='your-secret-key'
```

## Security Considerations

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration
- Environment variables for sensitive data
- Non-root container users
- Resource limits in Kubernetes

## Monitoring

- Health check endpoints: `/health`
- Prometheus metrics integration ready
- OpenTelemetry for distributed tracing
