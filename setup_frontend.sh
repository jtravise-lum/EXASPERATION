#!/bin/bash

set -e

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up EXASPERATION frontend environment...${NC}"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
PY_VERSION="$PY_MAJOR.$PY_MINOR"

# Simple integer comparison
if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 8 ]); then
    echo -e "${RED}Python 3.8 or higher is required. You have Python $PY_VERSION.${NC}"
    exit 1
fi

echo -e "${GREEN}Python $PY_VERSION detected.${NC}"

# Create frontend virtual environment if it doesn't exist
if [ ! -d "frontend_venv" ]; then
    echo -e "${YELLOW}Creating frontend environment...${NC}"
    python3 -m venv frontend_venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating frontend virtual environment...${NC}"
source frontend_venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing frontend dependencies...${NC}"
pip install --upgrade pip
pip install -r frontend.requirements.txt

# Verify Streamlit installation
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}Streamlit not found in PATH, installing explicitly...${NC}"
    pip install streamlit
fi

# Create .env.frontend file if it doesn't exist
if [ ! -f ".env.frontend" ]; then
    echo -e "${YELLOW}Creating .env.frontend file from template...${NC}"
    cp .env.frontend.example .env.frontend
    echo -e "${GREEN}Please edit the .env.frontend file to configure the frontend.${NC}"
fi

# Ensure frontend directories exist
if [ ! -d "frontend/assets/css" ]; then
    echo -e "${YELLOW}Creating frontend asset directories...${NC}"
    mkdir -p frontend/assets/css
    mkdir -p frontend/assets/images
    mkdir -p frontend/assets/js
fi

echo -e "${GREEN}Frontend setup complete!${NC}"
echo -e "${GREEN}To activate the frontend virtual environment, run:${NC}"
echo -e "source frontend_venv/bin/activate"
echo -e "${GREEN}To start the frontend application, run:${NC}"
echo -e "streamlit run frontend/app.py"
echo -e "${GREEN}Access the application at:${NC}"
echo -e "http://localhost:8501"