#!/bin/bash
# Install AI Backend Dependencies
# Usage: ./install_backends.sh

set -e

echo "=== Installing AI Backend Dependencies ==="
echo ""

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found. Installing via pip..."
    pip install uv
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing backend libraries..."
uv pip install openai pyautogen magentic docker anthropic cryptography

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "
import openai
import pyautogen
import magentic
import docker
import anthropic
import cryptography
print('✓ All backends installed successfully')
print('  - OpenAI:', openai.__version__)
print('  - AutoGen:', pyautogen.__version__)
print('  - Magentic:', magentic.__version__)
print('  - Docker:', docker.__version__)
print('  - Anthropic:', anthropic.__version__)
print('  - Cryptography:', cryptography.__version__)
"

echo ""
echo "✅ Installation complete!"
echo ""
echo "To use the backends:"
echo "  source .venv/bin/activate"
echo "  python -m reusable.cli status"
echo ""
echo "For vLLM setup, see: reusable/BACKEND_SETUP.md"
