# Quick Start - AI Assistant

## 1. Set API Key (30 seconds)

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

That's it! The AI assistant will auto-detect it.

## 2. Check Status

```bash
python -m reusable.cli status
```

## 3. Use It!

### Command Line

```bash
# Audit code
python -m reusable.cli audit app/main.py

# Repair issue
python -m reusable.cli repair "Function is slow" app/main.py

# Optimize
python -m reusable.cli optimize app/main.py

# Learn from codebase
python -m reusable.cli learn app/ architecture
```

### Python Code

```python
from reusable import get_ai_assistant, audit_file

# Simple function (auto-configures)
result = audit_file("app/main.py", audit_type="security")
print(result['findings'])

# Or get assistant
assistant = get_ai_assistant()
if assistant:
    result = assistant.audit("app/main.py")
```

## Configure Backend

```bash
# Interactive
python -m reusable.cli configure

# Direct
python -m reusable.cli configure openai
```

## That's It!

See [CONFIGURATION.md](./CONFIGURATION.md) for more details.
