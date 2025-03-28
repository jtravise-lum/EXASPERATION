#!/bin/bash
# Script to start the EXASPERATION API server in the background

# Navigate to the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${PROJECT_ROOT}" || exit 1

# Configuration
API_HOST="0.0.0.0"  # Listen on all interfaces
API_PORT=8888       # Default port from config
API_LOG_DIR="${PROJECT_ROOT}/logs"  # Directory for logs
API_LOG_FILE="api_server.log"
PID_FILE="${PROJECT_ROOT}/scripts/run/api_server.pid"

# Ensure log directory exists
mkdir -p "$API_LOG_DIR"

# Check if server is already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo "API server is already running with PID $PID"
        echo "To stop the server, run: ${SCRIPT_DIR}/stop_api_server.sh"
        exit 1
    else
        echo "Removing stale PID file"
        rm "$PID_FILE"
    fi
fi

# Check if API virtual environment exists, create if not
if [ ! -d "${PROJECT_ROOT}/api_venv" ]; then
    echo "Creating API virtual environment..."
    python3 -m venv "${PROJECT_ROOT}/api_venv"
    source "${PROJECT_ROOT}/api_venv/bin/activate"
    pip install -r "${PROJECT_ROOT}/frontend.requirements.txt"
else
    # Activate the API virtual environment
    source "${PROJECT_ROOT}/api_venv/bin/activate"
fi

# Start the API server in the background
echo "Starting EXASPERATION API server on $API_HOST:$API_PORT"
echo "Logs will be written to $API_LOG_DIR/$API_LOG_FILE"

# Export DEBUG_MODE for development
export DEBUG_MODE=True

# Start the server and redirect output to log file
nohup python -m frontend.api.main --host "$API_HOST" --port "$API_PORT" > "$API_LOG_DIR/$API_LOG_FILE" 2>&1 &

# Save the PID
echo $! > "$PID_FILE"
echo "API server started with PID $(cat "$PID_FILE")"
echo "To stop the server, run: ${SCRIPT_DIR}/stop_api_server.sh"

# Display the URL for accessing the API
echo ""
echo "API is now available at:"
echo "  - API Endpoints: http://$API_HOST:$API_PORT/v1/"
echo "  - API Documentation: http://$API_HOST:$API_PORT/v1/docs"
echo "  - Health Check: http://$API_HOST:$API_PORT/health"
echo ""
echo "Tail the logs with: tail -f $API_LOG_DIR/$API_LOG_FILE"
