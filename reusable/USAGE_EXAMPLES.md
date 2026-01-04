# AI Assistant Usage Examples

## Quick Setup

```bash
# 1. Set API key
export OPENAI_API_KEY="sk-your-key-here"

# 2. Check status
python -m reusable.cli status

# 3. Configure backend (optional)
python -m reusable.cli configure
```

## Command Line Usage

### Check Status
```bash
python -m reusable.cli status
```
Shows:
- Current backend
- Available backends (with API keys)
- Assistant availability
- Config file location

### Configure Backend
```bash
# Interactive
python -m reusable.cli configure

# Direct
python -m reusable.cli configure openai
python -m reusable.cli configure anthropic
```

### Audit Code
```bash
# Code audit
python -m reusable.cli audit app/main.py

# Security audit
python -m reusable.cli audit app/main.py security

# Performance audit
python -m reusable.cli audit app/main.py performance

# Config audit
python -m reusable.cli audit config.json config
```

### Repair Issues
```bash
# Repair with issue description
python -m reusable.cli repair "Function is too slow" app/main.py

# Repair without file (general advice)
python -m reusable.cli repair "Memory leak in Python code"
```

### Optimize Code
```bash
# Performance optimization
python -m reusable.cli optimize app/main.py performance

# Memory optimization
python -m reusable.cli optimize app/main.py memory

# Security optimization
python -m reusable.cli optimize app/main.py security
```

### Learn from Codebase
```bash
# Learn architecture
python -m reusable.cli learn app/ architecture

# Learn patterns
python -m reusable.cli learn app/ "design patterns"

# Learn from specific file
python -m reusable.cli learn app/main.py
```

### Update Dependencies
```bash
# Analyze requirements.txt
python -m reusable.cli update requirements.txt

# General dependency update
python -m reusable.cli update
```

## Python API Usage

### Simple Functions (Auto-Configure)

```python
from reusable import audit_file, repair_code, optimize_code

# Audit
result = audit_file("app/main.py", audit_type="security")
print(result['findings'])

# Repair
result = repair_code("Function is slow", file_path="app/main.py")
print(result['fix'])

# Optimize
result = optimize_code("app/main.py", opt_type="performance")
print(result['recommendations'])
```

### Get Assistant Instance

```python
from reusable import get_ai_assistant

# Auto-detect backend
assistant = get_ai_assistant()

# Specify backend
from reusable import AgentBackend
assistant = get_ai_assistant(backend=AgentBackend.ANTHROPIC)

# Use assistant
if assistant:
    result = assistant.audit("app/main.py", audit_type="code")
    result = assistant.repair("Issue description", "app/main.py")
    result = assistant.optimize("app/main.py", "performance")
    result = assistant.learn("app/", topic="architecture")
    result = assistant.update("dependencies", "requirements.txt")
```

### Configuration Management

```python
from reusable import AIConfig, AgentBackend

# Set backend
AIConfig.set_backend(AgentBackend.OPENAI)

# Auto-detect backend
backend = AIConfig.detect_backend()

# List available backends
available = AIConfig.list_available_backends()

# Get backend config
config = AIConfig.get_backend_config()
```

## Backend Configuration

### Environment Variables (Recommended)

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# AutoGen
export AUTOGEN_API_KEY="..."

# Magentic One
export MAGENTIC_ONE_API_KEY="..."
```

### Configuration File

Location: `~/.network_observability_ai_config.json`

```json
{
  "backend": "openai",
  "backend_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

### Programmatic Configuration

```python
from reusable import AIConfig, AgentBackend

# Set backend
AIConfig.set_backend(AgentBackend.OPENAI)

# Save custom config
config = {
    "backend": "openai",
    "backend_config": {
        "model": "gpt-4-turbo",
        "temperature": 0.5
    }
}
AIConfig.save_config(config)
```

## Complete Example

```python
#!/usr/bin/env python3
from reusable import get_ai_assistant

# Get assistant (auto-configures)
assistant = get_ai_assistant()

if assistant:
    # Audit code
    audit_result = assistant.audit("app/main.py", audit_type="code")
    print("Audit:", audit_result.get('findings', 'No findings'))
    
    # Optimize
    opt_result = assistant.optimize("app/main.py", "performance")
    print("Optimization:", opt_result.get('recommendations', 'No recommendations'))
    
    # Learn
    learn_result = assistant.learn("app/", topic="architecture")
    print("Knowledge:", learn_result.get('knowledge', 'No knowledge'))
else:
    print("Assistant not available. Set API key first.")
```

## Troubleshooting

### "Assistant not available"
1. Check API key: `echo $OPENAI_API_KEY`
2. Run status: `python -m reusable.cli status`
3. Configure: `python -m reusable.cli configure`

### "Backend not available"
- Check environment variables
- Try different backend: `python -m reusable.cli configure anthropic`
- See available backends: `python -m reusable.cli status`
