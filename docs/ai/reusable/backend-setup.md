# Backend Setup Guide

This guide explains how to set up and configure each AI backend for the network observability platform.

## Supported Backends

1. **OpenAI** - For OpenAI API and vLLM setups
2. **Microsoft AutoGen** - Multi-agent framework
3. **Magentic One** - Microsoft's agentic framework
4. **Docker Cagent** - Containerized agent execution
5. **Anthropic** - Claude API

## Installation

### All Backends

```bash
# Using uv (recommended)
uv pip install --system -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### Individual Backends

```bash
# OpenAI (for vLLM)
uv pip install --system openai

# Microsoft AutoGen
uv pip install --system pyautogen

# Magentic One
uv pip install --system magentic

# Docker Cagent
uv pip install --system docker

# Anthropic
uv pip install --system anthropic
```

## Configuration

### OpenAI (vLLM Setup)

For vLLM (local OpenAI-compatible server):

```bash
# Set vLLM endpoint
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="dummy-key"  # vLLM doesn't require real key
```

Or in code:
```python
from reusable import AIConfig

config = {
    "backend": "openai",
    "backend_config": {
        "api_base": "http://localhost:8000/v1",
        "api_key": "dummy-key",
        "model": "your-model-name"
    }
}
AIConfig.save_config(config)
```

### Microsoft AutoGen

```bash
export AUTOGEN_API_KEY="your-key"
```

Or configure in code:
```python
from reusable import AIConfig, AgentBackend

AIConfig.set_backend(AgentBackend.AUTOGEN)
```

### Magentic One

```bash
export MAGENTIC_ONE_API_KEY="your-key"
```

### Docker Cagent

Requires Docker to be running:
```bash
# Check Docker
docker ps

# No additional API key needed
```

### Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## vLLM Integration

### Starting vLLM Server

```bash
# Example: Start vLLM server
python -m vllm.entrypoints.openai.api_server \
    --model your-model \
    --port 8000 \
    --api-key dummy-key
```

### Using with AI Assistant

```python
from reusable import get_ai_assistant, AgentBackend
import os

# Set vLLM endpoint
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "dummy-key"

# Get assistant (will use vLLM)
assistant = get_ai_assistant(backend=AgentBackend.OPENAI)

if assistant:
    result = assistant.audit("app/main.py")
```

### vLLM Configuration File

Create `~/.network_observability_ai_config.json`:

```json
{
  "backend": "openai",
  "backend_config": {
    "api_base": "http://localhost:8000/v1",
    "api_key": "dummy-key",
    "model": "your-model-name",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

## Verification

### Check Installation

```bash
python3 -c "
import openai
import pyautogen
import magentic
import docker
import anthropic
print('✓ All backends installed')
"
```

### Check Status

```bash
python -m reusable.cli status
```

### Test Backend

```python
from reusable import get_ai_assistant, AgentBackend

# Test OpenAI/vLLM
assistant = get_ai_assistant(backend=AgentBackend.OPENAI)
if assistant and assistant.agent.is_available():
    print("✓ OpenAI/vLLM backend working")
    response = assistant.agent.chat("Hello!")
    print(response)
```

## Troubleshooting

### "Module not found"

Install missing backend:
```bash
uv pip install --system <backend-name>
```

### "Backend not available"

1. Check API key is set: `echo $OPENAI_API_KEY`
2. Check vLLM is running: `curl http://localhost:8000/v1/models`
3. Run status: `python -m reusable.cli status`

### vLLM Connection Issues

1. Verify vLLM is running:
   ```bash
   curl http://localhost:8000/v1/models
   ```

2. Check endpoint in config:
   ```bash
   cat ~/.network_observability_ai_config.json
   ```

3. Test connection:
   ```python
   import openai
   client = openai.OpenAI(
       base_url="http://localhost:8000/v1",
       api_key="dummy-key"
   )
   models = client.models.list()
   print([m.id for m in models])
   ```

## Backend Priority

The system checks backends in this order:

1. Environment variables (highest priority)
2. Configuration file (`~/.network_observability_ai_config.json`)
3. Default (OpenAI)

## Next Steps

- See [Configuration](./configuration.md) for detailed configuration
- See [Usage Examples](./usage-examples.md) for usage examples
- Run `python -m reusable.cli configure` for interactive setup
