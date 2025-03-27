# EXASPERATION Caddy Configuration

This document outlines the setup for using Caddy as a reverse proxy for the EXASPERATION application, enabling HTTPS access via the domain exp.travise.net.

## Caddy Overview

Caddy is a powerful, enterprise-ready, open source web server with automatic HTTPS written in Go. It's designed to be easy to use, with automatic HTTPS certificate provisioning and renewal through Let's Encrypt.

## Configuration

### 1. Basic Caddyfile

Create a file named `Caddyfile` in the project root with the following content:

```
exp.travise.net {
    reverse_proxy localhost:8501
    tls {
        protocols tls1.2 tls1.3
    }
    encode gzip zstd
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        X-XSS-Protection "1; mode=block"
        Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; font-src 'self'; object-src 'none'; media-src 'self'; frame-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self';"
    }
    log {
        output file /var/log/caddy/exp.travise.net.log {
            roll_size 10MB
            roll_keep 10
            roll_keep_for 720h
        }
    }
}
```

### 2. Docker Configuration

Add Caddy to the existing Docker Compose setup:

```yaml
version: '3'
services:
  # Existing services...
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - EXASPERATION_API_URL=http://api:8000
    depends_on:
      - api
    restart: always
    volumes:
      - ./frontend:/app
      
  caddy:
    image: caddy:2.6.4
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
      - ./logs/caddy:/var/log/caddy
    restart: always
    depends_on:
      - frontend

volumes:
  caddy_data:
  caddy_config:
```

### 3. Standalone Caddy Installation

If running Caddy as a standalone service on the host:

1. Install Caddy:

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

2. Place the Caddyfile at `/etc/caddy/Caddyfile`

3. Enable and start the Caddy service:

```bash
sudo systemctl enable caddy
sudo systemctl start caddy
```

## DNS Configuration

Ensure the DNS A/AAAA records for exp.travise.net point to the server's public IP address.

## Firewall Configuration

Ensure ports 80 and 443 are open on the server firewall:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

## Testing the Configuration

1. Start the Streamlit application on port 8501:
   ```bash
   cd frontend
   streamlit run app.py
   ```

2. Start Caddy (if not using systemd or Docker):
   ```bash
   caddy run --config /etc/caddy/Caddyfile
   ```

3. Access the application at https://exp.travise.net

## Monitoring Caddy

View Caddy logs:

```bash
# If using systemd
sudo journalctl -u caddy -f

# If using the file-based logs from the Caddyfile
tail -f /var/log/caddy/exp.travise.net.log
```

## Troubleshooting

If you encounter issues with the Caddy setup:

1. **Certificate issues**: Check that ports 80 and 443 are not blocked by firewalls or other services.
   
2. **Proxy connection refused**: Ensure the Streamlit service is running on port 8501.

3. **DNS resolution**: Verify that exp.travise.net properly resolves to your server's IP address.

4. **Log errors**: Check Caddy logs for specific error messages.

5. **Permissions**: Ensure Caddy has permission to write to its data directory.

## Security Considerations

The provided Caddyfile includes several security headers that help protect against common web vulnerabilities. Additional security measures to consider:

1. Implement IP-based rate limiting for sensitive endpoints
2. Configure automatic banning of suspicious IPs
3. Set up monitoring for unusual traffic patterns
4. Perform regular security audits of the proxy configuration

## Updating Caddy

To update Caddy when new versions are released:

```bash
sudo apt update
sudo apt upgrade caddy
```

For Docker-based installations, update the image tag in the docker-compose.yml file.