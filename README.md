# Microservices Platform

A production-ready microservices architecture built with FastAPI, PostgreSQL, RabbitMQ, Docker, and Kubernetes.

## 🏗️ Architecture

This project implements a distributed microservices system with:

- **User Service**: User authentication and profile management
- **Product Service**: Product catalog management  
- **Order Service**: Order processing and management

## 🚀 Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | FastAPI (Python) |
| **Database** | PostgreSQL 15 |
| **Message Broker** | RabbitMQ 3 |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes |
| **API Gateway** | Nginx |

## 📁 Project Structure

```
root/
├── docs/                    # Documentation
│   ├── architecture/        # Architecture decisions
│   ├── api/                 # API documentation
│   └── user_manual/         # User guides
├── services/
│   ├── user_service/        # User management (✅ Complete)
│   ├── product_service/     # Product catalog
│   ├── order_service/       # Order processing
│   └── common/              # Shared utilities
├── docker/                  # Docker configurations
│   ├── docker-compose.yml   # Local development
│   └── Dockerfile.*         # Service images
├── k8s/                     # Kubernetes manifests
│   ├── deployments/         # Deployments
│   ├── services/            # Services
│   └── ingress/             # Ingress rules
└── tests/                   # Test suites
    ├── functional/          # Functional tests
    └── performance/         # Load tests
```

## 🛠️ Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Poetry (optional, for local development)

### Run with Docker Compose

```bash
cd docker
docker-compose up -d
```

Access the services:
- **User Service API**: http://localhost:8001
- **API Gateway**: http://localhost:80
- **RabbitMQ Management**: http://localhost:15672
- **PostgreSQL**: localhost:5432

### API Documentation

Each service provides interactive API documentation:
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

## 🧪 Testing

### Functional Tests

```bash
cd tests
pytest functional/
```

### Performance Tests

```bash
cd tests/performance
locust -f locustfile.py --host=http://localhost:8001
```

## ☸️ Kubernetes Deployment

### Build Images

```bash
docker build -t microservices/user-service:latest -f docker/Dockerfile.user_service .
docker push microservices/user-service:latest
```

### Apply Manifests

```bash
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress/
```

### Create Secrets

```bash
kubectl create secret generic db-secret \
  --from-literal=url='postgresql://user:pass@host:5432/db'

kubectl create secret generic jwt-secret \
  --from-literal=key='your-secret-key'
```

## 📚 Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [API Documentation](docs/api/user_service.md)
- [User Manual](docs/user_manual/getting_started.md)

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Environment-based configuration
- Non-root container users
- Resource limits in Kubernetes

## 📊 Monitoring

- Health check endpoints: `/health`
- Prometheus metrics ready
- OpenTelemetry integration ready

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License

---

Built with ❤️ using FastAPI and modern cloud-native technologies