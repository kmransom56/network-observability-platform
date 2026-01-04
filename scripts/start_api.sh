#!/bin/bash
# Start Network Observability Platform API Server
# Uses port-manager to find and register port

set -e

# Find available port
PORT=$(port-manager find)

# Register port
port-manager register $PORT "Network Observability Platform API" "FastAPI server for network observability and AI assistant endpoints"

# Export port for application
export PORT=$PORT

echo "Starting API server on port $PORT"
echo "API Documentation: http://localhost:$PORT/docs"
echo "AI Assistant UI: http://localhost:$PORT/app/static/ai_assistant.html"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Start server
python app/main.py
