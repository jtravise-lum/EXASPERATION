#!/bin/bash
# Script to start all EXASPERATION components

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting EXASPERATION services...${NC}"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Create required directories
mkdir -p logs/caddy

# Start the Docker services
echo -e "${YELLOW}Starting Docker services...${NC}"
docker-compose up -d
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to start Docker services. See error above.${NC}"
    exit 1
fi

# Check if Caddy is installed
if ! command -v caddy &> /dev/null; then
    echo -e "${RED}Caddy is not installed. Please install Caddy first.${NC}"
    echo -e "${YELLOW}You can install Caddy with:${NC}"
    echo -e "sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https"
    echo -e "curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg"
    echo -e "curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list"
    echo -e "sudo apt update && sudo apt install caddy"
    exit 1
fi

# Check if Caddy service is running systemd
if systemctl is-active caddy >/dev/null 2>&1; then
    echo -e "${YELLOW}Caddy is running as a system service. Reloading configuration...${NC}"
    # Copy the Caddyfile to the system location
    sudo cp Caddyfile /etc/caddy/Caddyfile
    # Reload Caddy
    sudo systemctl reload caddy
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to reload Caddy. See error above.${NC}"
        echo -e "${YELLOW}You can check the Caddy error logs with: sudo journalctl -u caddy -e${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Caddy is not running as a system service. Starting Caddy manually...${NC}"
    caddy stop
    caddy run --config Caddyfile &
    CADDY_PID=$!
    echo $CADDY_PID > caddy.pid
    echo -e "${GREEN}Caddy started with PID $CADDY_PID${NC}"
fi

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 5

# Display service status
echo -e "${GREEN}EXASPERATION services started!${NC}"
echo -e "${YELLOW}ChromaDB is running at: http://localhost:8000${NC}"
echo -e "${YELLOW}API is running at: http://localhost:8888${NC}"
echo -e "${YELLOW}Frontend is running at: http://localhost:8501${NC}"
echo -e "${YELLOW}Application is accessible at: https://exp.travise.net${NC}"

echo -e "${YELLOW}To stop all services, run: ./stop_all.sh${NC}"