# AI Assistant Configuration Guide

## Quick Start

### 1. Set Environment Variable (Easiest)

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

That's it! The AI assistant will auto-detect and use it.

### 2. Use Configuration Command

```bash
# Interactive configuration
python -m reusable.cli configure

# Or direct
python -m reusable.cli configure openai
```

### 3. Programmatic Configuration

```python
from reusable import AIConfig, AgentBackend

# Set backend
AIConfig.set_backend(AgentBackend.OPENAI)

# Or use auto-detection (default)
backend = AIConfig.detect_backend()  # Auto-detects from env vars
```

## Backend Options

### OpenAI (Default)
```bash
export OPENAI_API_KEY="sk-..."
```

### Anthropic
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### AutoGen
```bash
export AUTOGEN_API_KEY="your-key"
```

### Magentic One
```bash
export MAGENTIC_ONE_API_KEY="your-key"
```

## Configuration File

Configuration is stored in: `~/.network_observability_ai_config.json`

Example:
```json
{
  "backend": "openai",
  "backend_config": {
    "model": "gpt-4",
    "temperature": 0.7
  }
}
```

## Simple Usage

### Command Line

```bash
# Check status
python -m reusable.cli status

# Audit code
python -m reusable.cli audit app/main.py

# Repair issue
python -m reusable.cli repair "Function is slow" app/main.py

# Optimize
python -m reusable.cli optimize app/main.py performance

# Learn from codebase
python -m reusable.cli learn app/ architecture

# Update dependencies
python -m reusable.cli update requirements.txt
```

### Python Code

```python
from reusable import get_ai_assistant, audit_file, repair_code

# Simple functions (auto-configures)
result = audit_file("app/main.py", audit_type="security")
result = repair_code("Function is slow", file_path="app/main.py")

# Or get assistant instance
assistant = get_ai_assistant()
if assistant:
    result = assistant.audit("app/main.py")
```

## Auto-Detection

The system automatically detects available backends in this order:

1. Environment variables (highest priority)
2. Configuration file
3. Default to OpenAI

## Status Check

```bash
python -m reusable.cli status
```

Shows:
- Current backend
- Available backends (with API keys)
- Assistant availability
- Config file location

## Troubleshooting

### "Agent framework not available"

1. Check API key is set:
   ```bash
   echo $OPENAI_API_KEY
   ```

2. Check status:
   ```bash
   python -m reusable.cli status
   ```

3. Configure manually:
   ```bash
   python -m reusable.cli configure
   ```

### "No API key found"

The assistant will prompt you to enter an API key interactively, or you can:

1. Set environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

2. Use SecureKeyManager:
   ```python
   from reusable import SecureKeyManager
   km = SecureKeyManager(app_name="network_observability")
   km.save_key("openai_api_key", "sk-...", env_var_name="OPENAI_API_KEY")
   ```

## Advanced Configuration

### Custom Backend Config

```python
from reusable import AIConfig, AgentBackend

config = {
    "backend": "openai",
    "backend_config": {
        "model": "gpt-4-turbo",
        "temperature": 0.5,
        "max_tokens": 2000
    }
}

AIConfig.save_config(config)
```

### Multiple Backends

You can switch backends dynamically:

```python
from reusable import get_ai_assistant, AgentBackend

# Use OpenAI
assistant_openai = get_ai_assistant(backend=AgentBackend.OPENAI)

# Use Anthropic
assistant_anthropic = get_ai_assistant(backend=AgentBackend.ANTHROPIC)
```
