# AGENTS.md - Network & Infrastructure Project

This file provides instructions for AI agents working with network infrastructure code.

## Project Focus
Network device management, topology visualization, Fortinet integration, or multi-vendor network automation.

## Key Guidelines

### Network Device Integration
- **Primary APIs**: FortiManager, Meraki Dashboard, SNMP
- **Configuration Files**: Device-specific configs in `configs/` or `network-configs/`
- **Topology Data**: Device relationships stored in Neo4j or JSON topology files
- **VLAN/Interface Management**: Consistent naming conventions across devices

### Code Organization
- Network device APIs in `api/` or `services/` directories
- Topology visualization in `frontend/` or `ui/` (typically React)
- Configuration management in `config/` or `scripts/config/`
- Integration tests in `tests/network/` or `integration-tests/`

### Development Workflow
```bash
# Environment setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start development services
docker-compose up -d
npm start  # If frontend exists

# Test network connectivity
python scripts/test_device_connectivity.py
```

### Network Security
- **Credentials**: Use environment variables, never commit credentials
- **API Keys**: Store in `.env` or secure vault
- **SSL/TLS**: Support corporate CA certificates (Zscaler compatibility)
- **Data Protection**: Handle device configs as sensitive data

### Testing
- Unit tests for device API clients
- Integration tests with test FortiManager/Meraki instances
- Topology validation tests
- Configuration drift detection tests

### Documentation
- Device API endpoint documentation
- Network topology diagrams
- Configuration examples
- Troubleshooting guides for common device issues

## See Also
- Main Guidelines: `/home/keith/CLAUDE.md`
- Network Systems: `chat-copilot/docs/` (Fortinet, Meraki integration)
