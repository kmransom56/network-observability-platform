# AI Assistant Integration Guide

This guide explains how the AI Assistant TUI, web interface, and code functions interact with the Network Observability Platform codebase.

## Overview

The AI Assistant provides **code-level assistance** for the Network Observability Platform itself. It can:
- **Audit** platform code for bugs, security issues, and best practices
- **Repair** issues in platform code automatically
- **Optimize** platform code for performance, memory, or cost
- **Learn** from the platform codebase to build knowledge
- **Update** platform dependencies

## Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Network Observability Platform                  │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   TUI        │  │   Web UI     │  │   REST API   │ │
│  │ (reusable/   │  │ (app/static/ │  │ (app/api/    │ │
│  │  tui.py)     │  │  ai_assistant│  │  ai_assistant│ │
│  │              │  │  .html)      │  │  .py)        │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                  │         │
│         └─────────────────┼──────────────────┘         │
│                           │                            │
│                  ┌─────────▼─────────┐                 │
│                  │  reusable/         │                 │
│                  │  simple_ai.py      │                 │
│                  │  (Wrapper)         │                 │
│                  └─────────┬─────────┘                 │
│                            │                            │
│                  ┌─────────▼─────────┐                 │
│                  │  reusable/         │                 │
│                  │  ai_assistant.py   │                 │
│                  │  (Core Logic)      │                 │
│                  └─────────┬─────────┘                 │
│                            │                            │
│                  ┌─────────▼─────────┐                 │
│                  │  Platform Code   │                 │
│                  │  app/             │                 │
│                  │  reusable/        │                 │
│                  │  scripts/         │                 │
│                  └───────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## How It Works

### 1. TUI Interface (`reusable/tui.py`)

The TUI provides an interactive menu to work with platform code:

```bash
python -m reusable.tui
```

**Example Workflow:**
1. User selects "Audit code/file"
2. Enters: `app/main.py`
3. Selects audit type: `security`
4. AI Assistant reads `app/main.py`
5. Analyzes code for security issues
6. Returns findings and recommendations

**Code Path:**
```
TUI → simple_ai.audit_file() → AIAssistant.audit() → Reads app/main.py → AI Analysis → Results
```

### 2. Web Interface (`app/static/ai_assistant.html`)

The web UI provides the same functionality via browser:

1. Navigate to: `http://localhost:11047/app/static/ai_assistant.html`
2. Select "Audit" tab
3. Enter file path: `app/api/ai_assistant.py`
4. Select audit type: `code`
5. Click "Run Audit"
6. JavaScript calls `/api/ai/audit` endpoint
7. FastAPI endpoint calls `audit_file()` function
8. Results displayed in browser

**Code Path:**
```
Browser → POST /api/ai/audit → app/api/ai_assistant.py → simple_ai.audit_file() → AIAssistant.audit() → Results → JSON Response → Browser Display
```

### 3. REST API (`app/api/ai_assistant.py`)

Direct API access for automation:

```bash
# Audit platform code
curl -X POST http://localhost:11047/api/ai/audit \
  -H "Content-Type: application/json" \
  -d '{"target": "app/main.py", "audit_type": "security"}'

# Repair issue in platform code
curl -X POST http://localhost:11047/api/ai/repair \
  -H "Content-Type: application/json" \
  -d '{"issue": "CORS middleware allows all origins", "file_path": "app/main.py"}'

# Optimize platform code
curl -X POST http://localhost:11047/api/ai/optimize \
  -H "Content-Type: application/json" \
  -d '{"target": "app/api/ai_assistant.py", "optimization_type": "performance"}'
```

## Practical Examples

### Example 1: Auditing Platform Code

**Via TUI:**
```bash
$ python -m reusable.tui
> Select: 1 (Audit)
> File/directory: app/
> Audit type: security
```

**What happens:**
1. `AIAssistant.audit("app/", "security")` is called
2. Reads all Python files in `app/` directory
3. Analyzes for security vulnerabilities
4. Returns findings like:
   - "CORS allows all origins - security risk"
   - "No input validation on API endpoints"
   - "API keys stored in plain text"

### Example 2: Repairing Platform Issues

**Via Web UI:**
1. Navigate to "Repair" tab
2. Issue: "FastAPI app doesn't handle errors gracefully"
3. File: `app/main.py`
4. Click "Repair"

**What happens:**
1. `AIAssistant.repair()` reads `app/main.py`
2. Analyzes error handling
3. Suggests fixes:
   ```python
   # Add error handlers
   @app.exception_handler(Exception)
   async def global_exception_handler(request, exc):
       return JSONResponse(
           status_code=500,
           content={"error": str(exc)}
       )
   ```

### Example 3: Optimizing Platform Performance

**Via API:**
```python
import requests

response = requests.post(
    "http://localhost:11047/api/ai/optimize",
    json={
        "target": "app/api/ai_assistant.py",
        "optimization_type": "performance"
    }
)

# Returns recommendations like:
# - "Use async/await for I/O operations"
# - "Cache AI responses"
# - "Batch API calls"
```

### Example 4: Learning from Platform Architecture

**Via TUI:**
```bash
> Select: 4 (Learn from codebase)
> Source: app/
> Topic: architecture
```

**What happens:**
1. `AIAssistant.learn("app/", "architecture")` is called
2. Reads all files in `app/` directory
3. Analyzes structure, patterns, dependencies
4. Builds knowledge base:
   - "Platform uses FastAPI for REST API"
   - "AI Assistant integrated via reusable/ module"
   - "Static files served from app/static/"
   - "Port allocation follows port-manager protocol"

## File Operations

The AI Assistant operates on **actual files** in the platform:

### Supported Targets

- **Single Files**: `app/main.py`, `reusable/ai_assistant.py`
- **Directories**: `app/`, `reusable/`, `scripts/`
- **Configuration**: `requirements.txt`, `.env`, `pyproject.toml`

### What Gets Analyzed

When you audit `app/`:
1. Reads all `.py` files recursively
2. Analyzes imports, functions, classes
3. Checks for:
   - Security vulnerabilities
   - Performance issues
   - Code quality
   - Best practices
   - Dependencies

### Code Reading Process

```python
# From ai_assistant.py
def audit(self, target: str, audit_type: str = "code"):
    # Read file or directory
    if os.path.isfile(target):
        with open(target, 'r') as f:
            content = f.read()  # Reads actual file content
    elif os.path.isdir(target):
        content = self._analyze_directory(target)  # Reads all files in directory
    
    # Send to AI for analysis
    response = self.agent.chat(prompt, system_prompt)
    return {"findings": response}
```

## Integration Points

### 1. Platform Code Analysis

The AI Assistant can analyze:
- **FastAPI routes** (`app/api/ai_assistant.py`)
- **Main application** (`app/main.py`)
- **Reusable components** (`reusable/*.py`)
- **Configuration files** (`requirements.txt`, `.env`)
- **Scripts** (`scripts/*.sh`)

### 2. Platform Improvement

The AI Assistant can:
- **Fix bugs** in platform code
- **Optimize** slow endpoints
- **Secure** vulnerable code
- **Update** outdated dependencies
- **Document** complex code

### 3. Knowledge Building

The AI Assistant learns:
- Platform architecture
- Code patterns
- API structure
- Integration points
- Best practices used

## Usage Scenarios

### Scenario 1: Pre-Deployment Audit

```bash
# Audit entire platform before deployment
python -m reusable.tui
> Audit → app/ → security
> Review findings
> Fix critical issues
```

### Scenario 2: Performance Optimization

```bash
# Optimize slow API endpoints
curl -X POST http://localhost:11047/api/ai/optimize \
  -d '{"target": "app/api/ai_assistant.py", "optimization_type": "performance"}'
```

### Scenario 3: Dependency Updates

```bash
# Check for outdated dependencies
python -m reusable.tui
> Update → requirements.txt
> Review recommendations
> Apply updates
```

### Scenario 4: Code Learning

```bash
# Learn platform architecture for documentation
python -m reusable.tui
> Learn → app/ → architecture
> Use knowledge for documentation
```

## Backend Integration

The AI Assistant uses configured backends to analyze platform code:

- **OpenAI/vLLM**: Code analysis, suggestions
- **AutoGen**: Multi-agent code review
- **Magentic One**: Structured code analysis
- **Anthropic**: Security-focused audits

All backends operate on the **same platform codebase** - they just use different AI models/approaches.

## Summary

The AI Assistant is **integrated into** the Network Observability Platform to:
1. **Analyze** platform code (audit)
2. **Fix** platform issues (repair)
3. **Improve** platform performance (optimize)
4. **Learn** platform architecture (learn)
5. **Update** platform dependencies (update)

All operations work on **actual files** in the `network-observability-platform` repository, making it a **self-improving** platform that can audit, repair, and optimize itself.
