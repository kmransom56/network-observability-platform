# Application Setup Guide

This guide explains how to properly add and register the Network Observability Platform application following the port allocation protocol.

## Port Allocation Protocol

Following the system-wide port allocation protocol from AGENTS.md:

### 1. Find Available Port

```bash
PORT=$(port-manager find)
echo "Using Port: $PORT"
```

### 2. Register Port

```bash
port-manager register $PORT "Network Observability Platform API" "FastAPI server for network observability and AI assistant endpoints"
```

### 3. Check Existing Ports

```bash
port-manager list
```

## Starting the Application

### Option 1: Use Start Script (Recommended)

```bash
./scripts/start_api.sh
```

This script automatically:
- Finds an available port using `port-manager`
- Registers the port
- Starts the FastAPI server

### Option 2: Manual Start

```bash
# Find and register port
PORT=$(port-manager find)
port-manager register $PORT "Network Observability Platform API" "FastAPI server"

# Start server
export PORT=$PORT
source .venv/bin/activate
python app/main.py
```

### Option 3: Direct Start (Uses Default Port)

```bash
source .venv/bin/activate
python app/main.py
# Defaults to port 8000 if PORT env var not set
```

## Application Endpoints

Once started, the application provides:

- **API Root**: `http://localhost:$PORT/`
- **API Documentation**: `http://localhost:$PORT/docs` (Swagger UI)
- **ReDoc**: `http://localhost:$PORT/redoc`
- **Health Check**: `http://localhost:$PORT/health`
- **AI Assistant API**: `http://localhost:$PORT/api/ai/*`
- **AI Assistant Web UI**: `http://localhost:$PORT/app/static/ai_assistant.html`

## Port Registry

The port is registered in the global registry at `~/.config/port_registry.md`. You can view all registered ports:

```bash
port-manager list
```

## Environment Variables

```bash
# Port (auto-set by start script, or set manually)
export PORT=11000

# For vLLM backend
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="dummy-key"

# For other backends
export ANTHROPIC_API_KEY="sk-ant-..."
export AUTOGEN_API_KEY="..."
export MAGENTIC_ONE_API_KEY="..."
```

## Docker Deployment

If deploying with Docker, ensure the port is allocated:

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "${PORT:-11000}:8000"  # Use port-manager allocated port
    environment:
      - PORT=8000
```

## Verification

After starting, verify the application:

```bash
# Check health
curl http://localhost:$PORT/health

# Check API status
curl http://localhost:$PORT/api/ai/status

# View registered ports
port-manager list | grep "Network Observability"
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
port-manager list

# Find a different port
PORT=$(port-manager find)
port-manager register $PORT "Network Observability Platform API" "Description"
export PORT=$PORT
```

### Port Not Registered

If you start the app without using the start script, register the port manually:

```bash
port-manager register 8000 "Network Observability Platform API" "FastAPI server"
```

## Integration with Other Services

When integrating with other services (NeDi, database, etc.), ensure all ports are properly allocated:

```bash
# Check all registered ports
port-manager list

# Ensure no conflicts
netstat -tulpn | grep -E "11000|8000|3000"
```
