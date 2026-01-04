# vLLM Setup Guide

Complete guide for setting up vLLM with the network observability platform.

## Prerequisites

- vLLM server running (typically on port 8000)
- OpenAI Python library installed

## Quick Setup

### 1. Start vLLM Server

```bash
# Example: Start vLLM with your model
python -m vllm.entrypoints.openai.api_server \
    --model your-model-name \
    --port 8000 \
    --api-key dummy-key
```

### 2. Configure Environment

```bash
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="dummy-key"
```

### 3. Test Connection

```bash
# Check vLLM is running
curl http://localhost:8000/v1/models

# Test with Python
python3 -c "
import openai
client = openai.OpenAI(
    base_url='http://localhost:8000/v1',
    api_key='dummy-key'
)
models = client.models.list()
print('Available models:', [m.id for m in models])
"
```

### 4. Use with AI Assistant

```python
from reusable import get_ai_assistant, AgentBackend
import os

# Set vLLM endpoint
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "dummy-key"

# Get assistant
assistant = get_ai_assistant(backend=AgentBackend.OPENAI)

if assistant:
    # Use it!
    result = assistant.audit("app/main.py", audit_type="code")
    print(result['findings'])
```

## Configuration File Method

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

## Command Line Usage

```bash
# Set environment variables
export OPENAI_API_BASE="http://localhost:8000/v1"
export OPENAI_API_KEY="dummy-key"

# Use CLI
python -m reusable.cli audit app/main.py
python -m reusable.cli repair "Issue" app/main.py
python -m reusable.cli optimize app/main.py
```

## Advanced Configuration

### Custom vLLM Endpoint

```python
from reusable import AIConfig, AgentBackend

config = {
    "backend": "openai",
    "backend_config": {
        "api_base": "http://192.168.0.1:8000/v1",  # Custom IP
        "api_key": "dummy-key",
        "model": "your-model",
        "temperature": 0.5,
        "max_tokens": 4000
    }
}

AIConfig.save_config(config)
```

### Multiple vLLM Instances

```python
# Instance 1 (default)
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
assistant1 = get_ai_assistant(backend=AgentBackend.OPENAI)

# Instance 2 (different port)
os.environ["OPENAI_API_BASE"] = "http://localhost:8001/v1"
assistant2 = get_ai_assistant(backend=AgentBackend.OPENAI)
```

## Troubleshooting

### Connection Refused

```bash
# Check if vLLM is running
curl http://localhost:8000/v1/models

# If not, start vLLM:
python -m vllm.entrypoints.openai.api_server --model your-model --port 8000
```

### Wrong Model Name

```bash
# List available models
curl http://localhost:8000/v1/models | jq '.data[].id'

# Update config with correct model name
```

### Timeout Issues

Increase timeout in config:
```json
{
  "backend_config": {
    "timeout": 300.0
  }
}
```

## Verification

```bash
# Check status
python -m reusable.cli status

# Test connection
python3 << EOF
import openai
client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy-key"
)
response = client.chat.completions.create(
    model="your-model",
    messages=[{"role": "user", "content": "Hello!"}]
)
print("Response:", response.choices[0].message.content)
EOF
```

## Integration with Network Observability

```python
from reusable import get_ai_assistant
import os

# Configure for vLLM
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "dummy-key"

# Get assistant
assistant = get_ai_assistant()

# Audit network code
result = assistant.audit("app/network_discovery.py", audit_type="code")

# Optimize performance
result = assistant.optimize("app/device_manager.py", "performance")

# Learn from codebase
result = assistant.learn("app/", topic="network architecture")
```
