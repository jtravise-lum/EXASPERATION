#!/bin/bash
# Script to stop all EXASPERATION components

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping EXASPERATION services...${NC}"

# Stop Docker services
echo -e "${YELLOW}Stopping Docker containers...${NC}"
docker-compose down
if [ $? -ne 0 ]; then
    echo -e "${RED}Error stopping Docker services. See error above.${NC}"
else
    echo -e "${GREEN}Docker services stopped.${NC}"
fi

# Check if Caddy is running as a manual process
if [ -f caddy.pid ]; then
    CADDY_PID=$(cat caddy.pid)
    if ps -p $CADDY_PID > /dev/null; then
        echo -e "${YELLOW}Stopping manually started Caddy (PID $CADDY_PID)...${NC}"
        kill $CADDY_PID
        rm caddy.pid
        echo -e "${GREEN}Caddy stopped.${NC}"
    else
        echo -e "${YELLOW}Caddy process not found. It may have already been stopped.${NC}"
        rm caddy.pid
    fi
fi

echo -e "${GREEN}All services stopped.${NC}"