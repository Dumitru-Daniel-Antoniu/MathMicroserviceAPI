# MathMicroserviceAPI

### Overview

MathMicroserviceAPI is a FastAPI-based microservice that performs various mathematical operations - power, Fibonacci, factorial, square root and logarithm - 
with integrated monitoring, caching and persistence. It integrates Redis caching, SQLite for storage, and Prometheus + Grafana for real-time observability, 
while ensuring scalability and maintainability in production environments. All these functionalities are orchestrated via Docker.

### Features
- Caching: Redis stores and retrieve results for faster responses
- Database Integration: operation logs stored in SQLite via SQLAlchemy
- Monitoring & Metrics: Prometheus exposes metrics for requests, durations, cache hits/misses automatically
    - Visualizing Metrics: Grafana dashboards for operations insights
- Dockerized Deployment: deployable via Docker and docker-compose
- User Authentication: secure JWT-based login system with password hashing
- Logging messages: centralized logging with optional message streaming support via Redis streams

### Used Technologies
- Backend: FastAPI (Python)
- Pattern: MVCS (Models, Views, Controllers, Services)
- Database: SQLAlchemy + SQLite
- Cache: Redis
- Monitoring: Prometheus, Grafana
- Containerization: Docker
- Logging: Redis streams

### Setup and Run
1. Clone and Install
```
git clone https://github.com/Dumitru-Daniel-Antoniu/MathMicroserviceAPI.git
cd MathMicroserviceAPI
```

2. Run with Docker
```
docker-compose up --build
```

3. Access via localhost
- API: `http://localhost:8000`
- Metrics: `http://localhost:8000/statistics`
- Grafana: `http://localhost:3000` 
- Prometheus: `http://localhost:9090`

### Task distribution
Dumitru Daniel-Antoniu:
- caching
- containerization
- monitoring
- frontend
- debugging

Istrate Liviu:
- math microservices
- backend (APIs)
- database
- logging
- authorization
- models