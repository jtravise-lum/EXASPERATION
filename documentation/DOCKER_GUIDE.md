# EXASPERATION Docker Guide

This guide provides instructions for deploying the complete EXASPERATION system using Docker and Docker Compose.

## Overview

The EXASPERATION system consists of three main components, all containerized for easier deployment:

1. **ChromaDB** - Vector database on port 8000 (internal)
2. **API Backend** - FastAPI service on port 8888
3. **Frontend** - Streamlit interface on port 8501

The Docker configuration includes:

- Python 3.10 images for all components
- Environment configuration through Docker environment variables
- Health checks to ensure application availability
- Volume mounts for development and hot-reloading
- Container networking between frontend, API, and database services
- Port configuration: ChromaDB (8000), API (8888), Frontend (8501)

## Quick Start

To start the entire EXASPERATION stack including the frontend:

```bash
docker-compose up -d
```

This will launch three containers:
- ChromaDB vector database on port 8000 (internal only)
- API backend on port 8888
- Frontend on port 8501

## Accessing the Application

Once the containers are running, access the frontend at:

```
http://localhost:8501
```

## Configuration

### Environment Variables

The frontend container can be configured using the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| STREAMLIT_SERVER_PORT | Port for Streamlit server | 8501 |
| STREAMLIT_SERVER_HEADLESS | Run in headless mode | true |
| EXASPERATION_API_URL | API endpoint URL | http://api:8000/v1 |
| ENABLE_ANALYTICS | Enable usage analytics | false |
| ENABLE_AUTHENTICATION | Enable user authentication | false |
| ENABLE_ADVANCED_FILTERS | Enable advanced filtering | true |
| ENABLE_SUGGESTIONS | Enable query suggestions | true |

You can modify these in the `docker-compose.yml` file or override them when running the container.

## Development with Docker

### Hot-Reloading

The Docker Compose configuration includes volume mounts that enable hot-reloading during development:

```yaml
volumes:
  - ./frontend:/app/frontend
```

This means you can edit the frontend code on your host machine and see changes immediately reflected in the running container.

### Viewing Logs

To view logs from the frontend container:

```bash
docker-compose logs -f frontend
```

### Container Shell Access

To get a shell inside the running frontend container:

```bash
docker-compose exec frontend bash
```

## Health Checks

The frontend container includes a health check script that verifies the Streamlit server is responding properly. Docker will automatically monitor this health check and restart the container if it fails repeatedly.

To manually check the health status:

```bash
docker inspect --format='{{.State.Health.Status}}' exasperation_frontend_1
```

## Production Deployment Considerations

When deploying to production, consider the following adjustments:

1. Remove the volume mounts to ensure consistency
2. Set appropriate environment variables for production
3. Implement proper network security (internal networks, firewall rules)
4. Add SSL termination via a reverse proxy like Caddy or Nginx

Example production `docker-compose.override.yml`:

```yaml
version: '3'
services:
  frontend:
    volumes: []  # Remove development volume mounts
    environment:
      - ENABLE_ANALYTICS=true
      - STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
      - EXASPERATION_API_URL=http://api:8000/v1
    deploy:
      replicas: 2
      restart_policy:
        condition: any
        max_attempts: 5
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

## Troubleshooting

### Container Won't Start

Check the logs for errors:

```bash
docker-compose logs frontend
```

Verify the API container is running and accessible from the frontend container:

```bash
docker-compose exec frontend curl -I http://api:8000/health
```

### Connectivity Issues

The frontend container needs to connect to the API container. If there are connectivity issues:

1. Ensure all containers are running: `docker-compose ps`
2. Check network connectivity: `docker-compose exec frontend ping api`
3. Verify API is accessible: `docker-compose exec frontend curl -I http://api:8000/health`

### Health Check Failures

If health checks are failing, you can debug by running the health check manually:

```bash
docker-compose exec frontend python /app/frontend/healthcheck.py
```