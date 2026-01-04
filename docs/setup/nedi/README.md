# NeDi Integration Guide

Complete guide for integrating NeDi network discovery with the Network Observability Platform.

## Quick Start

**Get started in 10 minutes:**
- **[Quick Start Guide](./quickstart.md)** - Fast setup with automated scripts

## Complete Documentation

- **[Quick Start](./quickstart.md)** - 10-30 minute setup guide with all options
- **[Installation Guide](./installation.md)** - Detailed step-by-step installation reference
- **[Complete Overview](./complete.md)** - Architecture, technical details, and enhancements
- **[Integration Guide](./integration.md)** - Integrating NeDi with the platform

## What is NeDi?

NeDi is a network discovery engine that provides:
- SNMP-based topology discovery
- Device inventory management
- Network topology visualization
- Device metrics tracking (CPU, temperature, memory)

## What Gets Installed

✅ **NeDi Network Discovery Engine** - SNMP-based topology discovery  
✅ **240+ Vendor-Specific Icons** - FortiGate, FortiAP, FortiSwitch, and more  
✅ **Client Device Icons** - Mobile, laptop, desktop detection  
✅ **Enhanced Web Interface** - PHP with D3.js visualization  
✅ **MySQL Database** - Device inventory and history  
✅ **Device Metrics** - CPU, temperature, memory, OS tracking  

## Quick Setup (Recommended)

```bash
cd /home/keith/network-observability-platform
sudo ./scripts/setup-nedi-integration.sh
```

This automated script:
- Installs enhanced icon library
- Applies PHP web interface enhancements
- Verifies all components
- Sets up integration with the platform

## Next Steps

1. **Run Setup**: `sudo ./scripts/setup-nedi-integration.sh`
2. **Configure SNMP**: Add credentials for your network devices
3. **Run Discovery**: `sudo /var/nedi/nedi.pl`
4. **Access NeDi**: http://localhost/Topology-Map.php
5. **Integrate with Platform**: See [Application Setup](../application-setup.md)

## Support

- **NeDi Official**: https://www.nedi.ch/
- **NeDi Guide PDF**: See `docs/The NeDi Guide.pdf`
- **Troubleshooting**: See troubleshooting sections in each guide
