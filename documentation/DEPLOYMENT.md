# EXASPERATION Deployment Guide

This document provides instructions for deploying the EXASPERATION system with Docker and Caddy.

## System Architecture

EXASPERATION consists of three main components:

1. **ChromaDB** - Vector database running on port 8000 (container only)
2. **API Backend** - FastAPI service running on port 8888 (exposed to host)
3. **Frontend** - Streamlit interface running on port 8501 (exposed to host)
4. **Caddy** - Reverse proxy providing HTTPS access (running on host)

## Prerequisites

- Docker and Docker Compose
- Caddy web server (either as systemd service or standalone)
- SSL certificates for your domain

## Configuration Files

### Docker Compose

The `docker-compose.yml` file defines three services:

- `chromadb`: Vector database
- `api`: FastAPI backend
- `frontend`: Streamlit UI

Each service uses the host network mode to facilitate direct communication between containers and the Caddy reverse proxy running on the host.

### Caddyfile

The `Caddyfile` configures the reverse proxy to:

- Route all root requests to the Streamlit frontend (port 8501)
- Route `/v1/*` requests to the API backend (port 8888)
- Apply HTTPS with your SSL certificates
- Add security headers and compression

## Quick Start

1. **Start all services**:
   ```bash
   ./start_all.sh
   ```

2. **Access the application**:
   - Frontend UI: https://exp.travise.net/
   - API: https://exp.travise.net/v1/
   - API documentation: https://exp.travise.net/v1/docs

3. **Stop all services**:
   ```bash
   ./stop_all.sh
   ```

## Manual Deployment Steps

If you prefer to deploy components individually:

1. **Start Docker services**:
   ```bash
   docker-compose up -d
   ```

2. **Configure Caddy**:
   - If running as systemd service:
     ```bash
     sudo cp Caddyfile /etc/caddy/Caddyfile
     sudo systemctl reload caddy
     ```
   - If running standalone:
     ```bash
     caddy run --config Caddyfile
     ```

## SSL Certificates

The configuration uses existing SSL certificates located at:
- `/home/johnt/caddy-docker/caddy/certs/exp.fullchain.pem`
- `/home/johnt/caddy-docker/caddy/certs/exp.privkey.pem`

To use different certificates:
1. Edit the `Caddyfile` and update the paths in the `tls` directive
2. Reload Caddy

## Port Mapping

| Service  | Container Port | Host Port | Purpose |
|----------|---------------|-----------|---------|
| ChromaDB | 8000          | 8000      | Vector database |
| API      | 8888          | 8888      | Backend API |
| Frontend | 8501          | 8501      | Streamlit UI |
| Caddy    | 80/443        | 80/443    | HTTP/HTTPS |

## Monitoring and Logs

- **Docker logs**:
  ```bash
  docker-compose logs -f
  ```

- **Caddy logs**:
  ```bash
  # If using systemd
  sudo journalctl -u caddy -f
  
  # If using the file logger
  tail -f logs/caddy/access.log
  ```

## Troubleshooting

### API Connection Issues

If the frontend can't connect to the API:
1. Verify the API container is running: `docker ps`
2. Check API logs: `docker-compose logs api`
3. Ensure the correct API URL is set in the frontend environment

### Caddy Certificate Issues

If Caddy has issues with the certificates:
1. Check certificate paths in the Caddyfile
2. Verify certificate permissions
3. Check Caddy logs

### Common Docker Issues

- **Port conflicts**: Make sure ports 8000, 8501, and 8888 are available
- **Container crashes**: Check logs with `docker-compose logs`

## Security Considerations

- The frontend, API, and ChromaDB are only accessible through the Caddy reverse proxy
- Security headers are applied to all responses
- All traffic is encrypted with HTTPS
- ChromaDB is not exposed to the public internet