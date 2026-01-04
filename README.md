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
- **NeDi Installation** - See [NeDi Setup Guide](#nedi-setup) below

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

## NeDi Setup

### Quick Start (10 minutes)

The Network Observability Platform requires NeDi for network topology discovery. Setup is automated:

```bash
# 1. Run the NeDi integration setup
sudo ./scripts/setup-nedi-integration.sh

# 2. Access NeDi at: http://localhost/Topology-Map.php

# 3. Configure SNMP on your network devices

# 4. Run discovery: sudo /var/nedi/nedi.pl
```

### Complete Setup Documentation

See the [NeDi Integration Guide](./docs/setup/nedi/README.md) for complete documentation:
- **[Quick Start](./docs/setup/nedi/quickstart.md)** - Get started in 10-30 minutes
- **[Installation Guide](./docs/setup/nedi/installation.md)** - Detailed step-by-step reference
- **[Complete Overview](./docs/setup/nedi/complete.md)** - Architecture and technical details
- **[Integration Guide](./docs/setup/nedi/integration.md)** - Platform integration

### What Gets Installed

✅ **NeDi Network Discovery Engine** - SNMP-based topology discovery  
✅ **240+ Vendor-Specific Icons** - FortiGate, FortiAP, FortiSwitch, and more  
✅ **Client Device Icons** - Mobile, laptop, desktop detection  
✅ **Enhanced Web Interface** - PHP with D3.js visualization  
✅ **MySQL Database** - Device inventory and history  
✅ **Device Metrics** - CPU, temperature, memory, OS tracking  

### Integration Features

- Vendor-specific device icons (136 FortiGate, 35 FortiAP, 69 FortiSwitch models)
- Automatic client device identification from MAC addresses
- D3.js topology visualization with interactive tooltips
- Real-time device metrics display
- API integration with the platform

### Setup Scripts

**Main Integration Script** (`scripts/setup-nedi-integration.sh`)
- Automates icon library installation
- Applies PHP enhancements
- Verifies all components
- Supports `--dry-run` mode for preview

**Enhancement Script** (`/home/keith/NeDi/apply-enhancements.py`)
- Adds vendor device detection
- Adds client device identification
- Enhances web interface
- Automatic backups and syntax verification

### AI Backend Setup

The platform supports multiple AI backends:

- **OpenAI** (including vLLM): `uv pip install --system openai`
- **Microsoft AutoGen**: `uv pip install --system pyautogen`
- **Magentic One**: `uv pip install --system magentic`
- **Docker Cagent**: `uv pip install --system docker`
- **Anthropic**: `uv pip install --system anthropic`

See [AI Backend Setup](./docs/ai/reusable/backend-setup.md) for detailed setup instructions.

## Documentation

Complete documentation is available in the [`docs/`](./docs/) directory:

### Setup & Installation
- **[Application Setup](./docs/setup/application-setup.md)** - Platform setup, port allocation, and deployment
- **[GitHub Setup](./docs/setup/github-setup.md)** - Repository setup and GitHub configuration
- **[NeDi Integration](./docs/setup/nedi/README.md)** - Complete NeDi installation and integration guide

### AI & Automation
- **[AI Assistant Overview](./docs/ai/README.md)** - AI Assistant features and architecture
- **[AI Integration Guide](./docs/ai/integration.md)** - How AI Assistant integrates with the platform
- **[Reusable Components](./docs/ai/reusable/README.md)** - Reusable AI components package

### Quick Links
- **[Documentation Index](./docs/README.md)** - Complete documentation index
- **[NeDi Quick Start](./docs/setup/nedi/quickstart.md)** - Get NeDi running in 10 minutes
- **[AI Assistant Quick Start](./docs/ai/reusable/quickstart-ai-assistant.md)** - Get AI Assistant running in 30 seconds

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

MIT License - See [LICENSE](./LICENSE) file for details.

## Status

🚧 **In Development** - Active development in progress
