# Network Observability Platform

A comprehensive network observability and management platform for enterprise network infrastructure.

## Overview

This platform provides real-time network monitoring, device discovery, topology visualization, and automated network management capabilities for multi-vendor network environments.

## Features

- **Multi-Vendor Support**: Fortinet (FortiGate, FortiSwitch, FortiAP), Cisco Meraki, and generic SNMP devices
- **Real-Time Discovery**: Automated device and client discovery via SNMP, REST APIs, and SSH
- **Device Identification**: MAC address OUI lookup, device type classification, and wireless client tracking
- **Topology Visualization**: Network topology mapping and visualization
- **API Integration**: RESTful APIs for network device management
- **Database Storage**: Persistent storage of network inventory and historical data
- **AI-Assisted Operations**: Audit, repair, update, optimize, and learn capabilities using AI agents

## Architecture

- **Backend**: Python (FastAPI) and Perl (NeDi integration)
- **Frontend**: React with Material-UI
- **Database**: MySQL/MariaDB for network inventory
- **Real-Time**: WebSocket support for live updates

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- MySQL/MariaDB
- Network device access (SNMP, SSH, REST API)

### Installation

```bash
# Clone the repository
git clone https://github.com/kmransom56/network-observability-platform.git
cd network-observability-platform

# Set up Python environment (using uv - recommended)
uv pip install --system -r requirements.txt

# Or using virtual environment
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Set up Node.js dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python scripts/init_db.py

# Configure AI backends (optional)
python -m reusable.cli configure
```

### AI Backend Setup

The platform supports multiple AI backends:

- **OpenAI** (including vLLM): `uv pip install --system openai`
- **Microsoft AutoGen**: `uv pip install --system pyautogen`
- **Magentic One**: `uv pip install --system magentic`
- **Docker Cagent**: `uv pip install --system docker`
- **Anthropic**: `uv pip install --system anthropic`

See [reusable/BACKEND_SETUP.md](./reusable/BACKEND_SETUP.md) for detailed setup instructions.

## Documentation

- [Device Discovery](./docs/device-discovery.md)
- [API Reference](./docs/api-reference.md)
- [Wireless Device Identification](./docs/wireless-identification.md)
- [AI Assistant](./reusable/README.md) - AI-assisted audit, repair, update, optimize, and learn
- [Reusable Components](./reusable/QUICKSTART.md) - Quick start guide

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Status

🚧 **In Development** - Active development in progress
