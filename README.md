# Country Explorer Application

## Overview

A full-stack application that provides comprehensive information about countries worldwide, including population statistics, geographical data, and user-contributed images. The system integrates with the public REST Countries API and offers a responsive web interface for exploration.

## Key Features

- Browse complete country data including names, regions, and demographics
- View population density calculations
- Upload and share favorite country images
- Efficient caching for improved performance

## Technical Stack

### Backend

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis with persistence

### Frontend
- **Framework**: React.js

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose, Kubernetes

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Node.js
- Python

## Quick Start with Docker

1. Clone the repository:

```
git clone https://github.com/StephenDsouza90/countries-of-the-world.git
cd countries-of-the-world
```

2. Start all services:

```
docker-compose up -d
```

3. Access the application:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8080

4. Stop the application:

```
docker-compose down
```

## Detailed Documentation

### Backend Architecture

**Database Layer**

- PostgreSQL relational database
- SQLAlchemy ORM with declarative models
- Session management
- Optimized bulk operations for data loading

**API Layer**

- RESTful endpoints with proper HTTP status codes
- Request validation using Pydantic models

**Caching Strategy**

- Country information (TTL: 1 hour)
- Frequent requests (TTL: 30 minutes)
- Image assets (TTL: 24 hours)
- Cache invalidation on data updates

**Data Pipeline**

- Extract: Fetch from REST Countries API
- Transform: Calculate population density, format data
- Load: Bulk upsert to PostgreSQL

## Deployment Options (Locally)

### Docker Compose

```
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Run specific service
docker-compose run --rm data_pipeline
```

### Kubernetes

1. Start Minikube cluster:

```
minikube start
```

2. Build images:
```
docker build -t data_pipeline:latest -f ./docker/Dockerfile.data_pipeline .
docker build -t backend:latest -f ./docker/Dockerfile.backend .
docker build -t frontend:latest -f ./docker/Dockerfile.frontend .
```

2. Load images:
```
minikube image load data-pipeline:latest
minikube image load backend:latest
minikube image load frontend:latest
```

Check if the images are available in Minikube:
```
minikube ssh
docker images
```

Incase you want to remove an image from minikube
```
docker rmi <image-id>
```

3. Deploy application:
```
kubectl apply -f k8s/redis 
kubectl apply -f k8s/postgres 
kubectl apply -f k8s/data-pipeline
kubectl apply -f k8s/backend
kubectl apply -f k8s/frontend
kubectl apply -f k8s/network
```

4. Access services via Port forwarding:
```
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8080:8080
```

## Testing

Run the complete test suite:

```
make test
```

### Test Coverage

- Unit tests for all core components
- Integration tests for API endpoints
- Mocked external API calls
