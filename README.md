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
- **Database**: MongoDB
- **Caching**: Redis

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

- MongoDB NoSQL database

To connect to DB

```
docker ps
docker exec -it countries-of-the-world-mongo-1 mongo
show dbs
use recruiting
show collections
db.countries.find().pretty()
```

**API Layer**

- RESTful endpoints with proper HTTP status codes
- Request validation using Pydantic models

**Caching Strategy**

- Country information
- Frequent requests
- Image assets

To connect to Redis

```
docker ps
docker exec -it countries-of-the-world-redis-1 redis-cli
KEYS *
GET <key>
```

**Data Pipeline**

- Extract: Fetch from REST Countries API
- Transform: Calculate population density, format data
- Load: Insert to MongoDB

## Deployment Options (Locally)

### Docker Compose

The `docker-compose.yml` file orchestrates the multi-container setup. It ensures that the services start in the correct order:

1. The **MongoDB** database container starts first and waits until it is healthy.
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
eval $(minikube docker-env)
docker build -t data-pipeline:latest -f ./docker/Dockerfile.data_pipeline .
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
kubectl apply -f k8s/mongo
kubectl apply -f k8s/data-pipeline
kubectl apply -f k8s/backend
kubectl apply -f k8s/frontend
kubectl apply -f k8s/network
```

Verify resources:

```
kubectl get pods
kubectl describe pod <pod-name> 
kubectl logs <pod-name>
```

```
kubectl exec -it <mongo-pod-name> -- mongo
```

The application uses an NGINX Ingress controller to route external traffic to the appropriate services within the Kubernetes cluster. The **Ingress** resource is defined in the `ingress.yml` file.

4. Access services via Port forwarding:

```
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8080:8080
```

5. Clear up resources 

Stop minikube

```
minikube stop
minikube delete
```

Delete commands

```
kubectl delete pod <pod-name>
kubectl delete deployment <deployment-name>     
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

backend/tests/test_api_handler.py .......                                                                               [ 36%]
data_pipeline/tests/test_client.py ..                                                                                   [ 47%]
data_pipeline/tests/test_handler.py ....                                                                                [ 68%]
internal/cache/tests/test_cache.py ....                                                                                 [ 89%]
internal/cache/tests/test_redis_client.py ..                                                                            [100%]

==================== 9 passed in 0.32s ====================
```