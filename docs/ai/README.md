# AI Assistant Documentation

Complete guide for the AI Assistant integration with the Network Observability Platform.

## Overview

The AI Assistant provides **code-level assistance** for the Network Observability Platform itself. It can:
- **Audit** platform code for bugs, security issues, and best practices
- **Repair** issues in platform code automatically
- **Optimize** platform code for performance, memory, or cost
- **Learn** from the platform codebase to build knowledge
- **Update** platform dependencies

## Quick Start

**Get started in 30 seconds:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
python -m reusable.cli status
```

## Documentation

### Integration & Architecture

- **[Integration Guide](./integration.md)** - How AI Assistant integrates with the platform
  - TUI, Web UI, and REST API interfaces
  - Code paths and architecture
  - Practical examples

### Reusable Components

The AI Assistant is built on reusable components that can be integrated into other projects:

- **[Reusable Components Overview](./reusable/README.md)** - Package overview and installation
- **[Quick Start](./reusable/quickstart.md)** - Get started in 5 minutes
- **[AI Assistant Quick Start](./reusable/quickstart-ai-assistant.md)** - AI Assistant specific quick start
- **[Configuration](./reusable/configuration.md)** - Backend configuration and setup
- **[Backend Setup](./reusable/backend-setup.md)** - Setting up AI backends (OpenAI, AutoGen, etc.)
- **[Usage Examples](./reusable/usage-examples.md)** - Command line and Python API examples
- **[vLLM Setup](./reusable/vllm-setup.md)** - Setting up vLLM for local AI inference

## Interfaces

### 1. TUI (Terminal User Interface)

```bash
python -m reusable.tui
```

Interactive menu for:
- Auditing code
- Repairing issues
- Optimizing performance
- Learning from codebase

### 2. Web Interface

Access at: `http://localhost:11047/app/static/ai_assistant.html`

Browser-based interface with tabs for:
- Audit
- Repair
- Optimize
- Learn
- Update

### 3. REST API

```bash
curl -X POST http://localhost:11047/api/ai/audit \
  -H "Content-Type: application/json" \
  -d '{"target": "app/main.py", "audit_type": "security"}'
```

## Supported Backends

- **OpenAI** (including vLLM)
- **Microsoft AutoGen**
- **Magentic One**
- **Docker Cagent**
- **Anthropic**

See [Backend Setup](./reusable/backend-setup.md) for configuration.

## Next Steps

1. **Set API Key**: `export OPENAI_API_KEY="sk-..."`
2. **Check Status**: `python -m reusable.cli status`
3. **Try It**: `python -m reusable.cli audit app/main.py`
4. **Read Integration Guide**: [integration.md](./integration.md)
