#!/bin/bash

set -e

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting EXASPERATION frontend...${NC}"

# Check if frontend_venv exists
if [ ! -d "frontend_venv" ]; then
    echo -e "${YELLOW}Frontend environment not found. Setting up now...${NC}"
    ./setup_frontend.sh
fi

# Activate the virtual environment
source frontend_venv/bin/activate

# Install streamlit explicitly if not available
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Installing Streamlit...${NC}"
    pip install streamlit
fi

# Run the application
echo -e "${GREEN}Starting Streamlit server...${NC}"
PYTHONPATH=$(pwd) streamlit run frontend/app.py