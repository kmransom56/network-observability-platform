# Network Observability Platform

A comprehensive network observability and management platform for enterprise network infrastructure.

## Overview

This platform provides real-time network monitoring, device discovery, topology visualization, and automated network management capabilities for multi-vendor network environments.

## Features

- **Multi-Vendor Support**: Fortinet (FortiGate, FortiSwitch, FortiAP), Cisco Meraki, and generic SNMP devices
- **Real-Time Discovery**: Automated device and client discovery via SNMP, REST APIs, and SSH
- **Device Identification**: MAC address OUI lookup, device type classification, and wireless client tracking
- **Topology Visualization**: Network topology mapping and visualization
- **API Integration**: RESTful APIs for network device management with 1,676+ verified endpoints
- **API Validation**: MCP-based validation of 814 Fortinet and 862 Meraki API endpoints
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

## MCP Server Integration

The platform includes integrated MCP (Model Context Protocol) server support for API validation and code generation:

### API Endpoint Documentation

The platform has offline access to 1,676+ network device API endpoints:

**Meraki API:** 862 endpoints
- GET operations: 468
- POST operations: 157
- PUT operations: 174
- DELETE operations: 63

**Fortinet (FNDN) API:** 814 endpoints
- FortiGate operations: 465
- FortiManager operations: 92
- FortiAnalyzer operations: 257

### Features

✅ **Device Operation Validation** - Validate operations before execution
✅ **Multi-Vendor Support** - FortiGate, FortiManager, FortiAnalyzer, Meraki
✅ **API Search** - Find endpoints by keyword across all vendors
✅ **Code Generation** - Auto-generate device API client code
✅ **AI Integration** - Claude, Cline, Cursor have access to real endpoints
✅ **Offline Documentation** - All endpoints available without internet

### Quick Start

```bash
# Test MCP integration
python3 api_validator.py

# Or check MCP status via API
curl http://localhost:8000/mcp/status

# Use in device management code
from api_validator import NetworkDeviceValidator
validator = NetworkDeviceValidator()
is_valid = validator.validate_device_operation("fortigate", "firewall")
```

### Documentation

- **[MCP Quick Start](./NETWORK_OBSERVABILITY_MCP_QUICK_START.md)** - 5-minute integration guide
- **[MCP Setup Guide](./MCP_INTEGRATION_SETUP.md)** - Comprehensive setup and configuration
- **[MCP Status](./MCP_INTEGRATION_COMPLETE.md)** - Integration verification and next steps

## Vendor-Specific Icon Mapping

The platform includes comprehensive vendor-specific icon mapping for network topology visualization.

### Features

✅ **Device Type Identification** - Automatically identifies FortiGate, FortiSwitch, FortiAP, Meraki, Cisco devices
✅ **Vendor-Specific Icons** - 336+ Fortinet icons (136 FortiGate models, 69 FortiSwitch, 35 FortiAP models)
✅ **Endpoint Detection** - Desktop, laptop, and mobile device identification
✅ **Vendor Color Coding** - Visual distinction by vendor (#E5A100 Fortinet, #00BCD4 Meraki, #0066CC Cisco)
✅ **Model-Specific Icons** - Detailed device representation (FG-3100D.svg, FSW-248D.svg, etc.)
✅ **Infrastructure vs Endpoints** - Clear visual hierarchy for device types

### Components

**Python Mapper** (`icon_vendor_mapper.py`):
```python
from icon_vendor_mapper import VendorIconMapper

mapper = VendorIconMapper()
icon_info = mapper.get_device_icon(sysname="FortiGate-3100D", model="FG-3100D")
# Returns: icon path, vendor, color, category, device type
```

**PHP NeDi Integration** (`nedi_topology_mapper.php`):
```php
require_once('nedi_topology_mapper.php');
$mapper = new NeDiTopologyMapper();
$html = $mapper->get_device_icon_html('FortiGate-3100D', 'FG-3100D', 32);
```

**NeDi Integration Module** (`nedi_topology_integration.py`):
```python
from nedi_topology_integration import NeDiTopologyIntegrator

integrator = NeDiTopologyIntegrator()
devices = integrator.get_topology_devices()
enhanced = integrator.enhance_devices_with_icons(devices)
integrator.export_topology_for_d3('/tmp/topology_d3.json')
```

### Your Network Devices

The following devices in your network are mapped to vendor-specific icons:

- **FortiGate-3100D** (192.168.0.254) → Fortinet Orange, firewall icon
- **FortiSwitch-248D** (10.255.1.2) → Fortinet Orange, switch icon
- **FortiAP-222B, FortiAP-231F** → Fortinet Orange, access_point icons

### Documentation

- **[Full Icon Mapping Guide](./ICON_MAPPING_GUIDE.md)** - Complete documentation and API reference
- **[Implementation Quick Reference](./VENDOR_ICON_IMPLEMENTATION.md)** - Step-by-step integration guide
- **[Icon Library](file:///var/nedi/icon_library/)** - 2,114+ SVG/PNG icons available

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
