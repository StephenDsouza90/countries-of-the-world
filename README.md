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

The `docker-compose.yml` file orchestrates the multi-container setup. It ensures that the services start in the correct order:

1. The **PostgreSQL** database container starts first and waits until it is healthy.
2. The **Data Pipeline** container runs to populate the database with data from the external API.
3. The **Backend** container starts, initializing the API and making it available for the frontend.
4. Finally, the **Frontend** container starts, providing the user interface for interacting with the application.

It is setup this way to avoid running into a race condition.

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

```
✗ make test

python3.10 -m pytest
==================== test session starts ====================
platform darwin -- Python 3.10.15, pytest-7.4.2, pluggy-1.5.0
plugins: anyio-3.7.1, mock-3.14.0
collected 9 items                                                                                                                                                                         

backend/tests/test_api.py ...                                                            [ 33%]
data_pipeline/tests/test_client.py ..                                                    [ 55%]
data_pipeline/tests/test_handler.py .                                                    [ 66%]
data_pipeline/tests/test_main.py .                                                       [ 77%]
data_pipeline/tests/test_processor.py ..                                                 [100%]

==================== 9 passed in 0.32s ====================
```
