# MCP Server Integration for Network Observability Platform

**Status:** Ready for Integration
**Location:** `/home/keith/network-observability-platform/`
**MCP Server:** `/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/mcp_server.py`

## Overview

Integrate the FNDN & Meraki API Documentation MCP Server with the Network Observability Platform to provide:

- ✅ **Claude Integration** - Accurate API endpoints for FortiGate and Meraki when using Claude for development
- ✅ **Cline Integration** - Real endpoint validation in Cline agent workflows
- ✅ **Ralph Integration** - Autonomous agent development with verified APIs
- ✅ **Antigravity IDE** - AI-assisted code generation with real endpoint data
- ✅ **Cursor IDE** - API endpoint suggestions and validation
- ✅ **Code Generation** - Auto-generate FortiGate/Meraki API client code
- ✅ **Endpoint Validation** - Validate device operations before deployment
- ✅ **Device Comparison** - Compare operations across FortiGate and Meraki

## Benefits for Network Observability Platform

### 1. **Device Management Development**
When building/extending device management integration:
- Search 465 FortiGate operations
- Get exact operation paths, resources, and parameters
- Search 862 Meraki endpoints
- Generate working API client code
- Validate operations before implementation
- Compare equivalent operations across vendors

### 2. **AI Tool Assistance**
When using Claude, Cline, or Cursor:
- Ask for FortiGate/Meraki API help with accurate endpoint data
- Get verified code generation
- Prevent errors from incorrect operation names
- Understand API structure before implementation

### 3. **Automation Safety**
Before deploying network changes:
- Validate all device operations against documentation
- Check endpoint availability for each vendor
- Ensure parameter compatibility
- Verify operation support across device versions

### 4. **Multi-Vendor Discovery**
When adding device support:
- Compare operations across FortiGate, Meraki, and SNMP
- Identify equivalent operations
- Map operations between vendors
- Find vendor-specific features

## Setup Instructions

### Step 1: Verify Files Are in Place

The integration files have been copied to the root directory:

```bash
cd /home/keith/network-observability-platform

# Verify files exist
ls -la mcp_client.py code_generator.py api_validator.py .env.template
```

Expected files:
- ✅ `mcp_client.py` (11 KB) - MCPClient for programmatic access
- ✅ `code_generator.py` (11 KB) - Auto-generate API client code
- ✅ `api_validator.py` (13 KB) - Device-specific validators
- ✅ `.env.template` (698 B) - Configuration template

### Step 2: Configure Environment

Create `.env` or copy from template:

```bash
cp .env.template .env
nano .env
```

Configuration options:

```bash
# MCP Server (required)
MCP_HOST=127.0.0.1
MCP_PORT=11503

# FortiGate Live API (optional)
FORTIGATE_HOST=192.168.1.1
FORTIGATE_USERNAME=admin
FORTIGATE_PASSWORD=admin

# Meraki Live API (optional)
MERAKI_API_KEY=your_key_here
MERAKI_ORG_ID=your_org_id

# Fortinet Manager (optional)
FORTIMANAGER_HOST=192.168.0.1
FORTIMANAGER_USERNAME=admin
FORTIMANAGER_PASSWORD=admin
```

### Step 3: Verify MCP Client in main.py

The MCP client is already initialized in `app/main.py`:

```python
# MCP Integration
try:
    from mcp_client import MCPClient
    mcp_client = MCPClient.from_env()
    mcp_stats = mcp_client.get_statistics()
    logger.info(f"MCP Server: {mcp_stats['meraki']['total_endpoints']} Meraki endpoints available")
    logger.info(f"MCP Server: {mcp_stats['fndn']['total_endpoints']} FNDN endpoints available")
except Exception as e:
    logger.warning(f"MCP Server initialization: {e}")
    mcp_client = None
```

### Step 4: Use API Validators in Device Code

Create device management integration with validation:

```python
from api_validator import FortiGateAPIValidator, MerakiAPIValidator, NetworkDeviceValidator

# Initialize validators
fg_validator = FortiGateAPIValidator()
meraki_validator = MerakiAPIValidator()
device_validator = NetworkDeviceValidator()

# Example: Validate before executing device operation
def execute_fortigate_operation(device_id, operation):
    # Validate operation exists
    is_valid, description = fg_validator.validate_endpoint(operation)

    if not is_valid:
        raise ValueError(f"FortiGate operation not supported: {operation}")

    # Safe to proceed with device API call
    return device_api.execute(device_id, operation)

# Example: Validate Meraki endpoint
def get_meraki_networks(org_id):
    # Validate endpoint
    is_valid, summary = meraki_validator.validate_endpoint(
        f"/organizations/{org_id}/networks",
        "GET"
    )

    if not is_valid:
        raise ValueError("Meraki endpoint not available")

    # Safe to proceed
    return meraki_api.get_networks(org_id)

# Example: Compare operations across vendors
def compare_device_capabilities(operation):
    comparison = device_validator.compare_vendors(operation)
    print(f"Operation {operation} available in: {comparison['available_in']}")
```

### Step 5: Configure for Claude Desktop

The MCP server is already configured in Claude Desktop. To verify:

```bash
cat ~/.config/Claude/claude_desktop_config.json | grep -A 10 "fndn-meraki-mcp"
```

If not present, add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fndn-meraki-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn",
        "run",
        "mcp_server.py"
      ],
      "env": {
        "MERAKI_API_KEY": "${MERAKI_API_KEY}",
        "MCP_PORT": "11503"
      }
    }
  }
}
```

### Step 6: Configure for Cline

Create `.cline/mcp.json` in application root:

```json
{
  "mcpServers": [
    {
      "name": "FNDN & Meraki API",
      "command": "python3",
      "args": [
        "/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/mcp_server.py"
      ],
      "env": {
        "MCP_PORT": "11503",
        "MERAKI_API_KEY": "${MERAKI_API_KEY}"
      }
    }
  ]
}
```

### Step 7: Configure for Antigravity

Add to `AGENTS.md`:

```markdown
## MCP Server Integration

### Device API Validation

All device API operations are automatically validated against MCP documentation:

1. **FortiGate Operations**
   - Validate operations exist
   - Check resource availability
   - Get operation descriptions

2. **Meraki API Endpoints**
   - Search endpoints by keyword
   - Get endpoint specifications
   - Validate endpoint paths

3. **Multi-Vendor Comparison**
   - Compare operations across vendors
   - Find equivalent operations
   - Identify vendor-specific features

### Available in Code

```python
from api_validator import NetworkDeviceValidator

validator = NetworkDeviceValidator()
is_valid, desc = validator.validate_device_operation("fortigate", "firewall")
```
```

## Usage Examples

### Example 1: Validate FortiGate Operations

When implementing FortiGate device management:
```python
from api_validator import FortiGateAPIValidator

validator = FortiGateAPIValidator()

# Validate before execution
operations = ["firewall", "system", "network"]
for op in operations:
    is_valid, desc = validator.validate_endpoint(op)
    if is_valid:
        print(f"✓ {op}: {desc}")
    else:
        print(f"✗ {op}: Not found")
```

### Example 2: Search FortiGate Operations

```python
from api_validator import FortiGateAPIValidator

validator = FortiGateAPIValidator()

# Search for firewall-related operations
firewall_ops = validator.get_endpoint_info("firewall")
print(f"Found {firewall_ops['total_results']} firewall operations")

for ep in firewall_ops['endpoints']:
    print(f"  {ep['operation']} ({ep['resource']})")
```

### Example 3: Validate Meraki Endpoints

```python
from api_validator import MerakiAPIValidator

validator = MerakiAPIValidator()

# Validate endpoint before use
is_valid, summary = validator.validate_endpoint(
    "/organizations/{organizationId}/networks",
    "GET"
)

if is_valid:
    print(f"✓ Endpoint valid: {summary}")
else:
    print("✗ Endpoint not found")
```

### Example 4: Search Meraki Endpoints

```python
from api_validator import MerakiAPIValidator

validator = MerakiAPIValidator()

# Get organization-related endpoints
org_endpoints = validator.get_endpoints_by_tag("organizations")
print(f"Organization endpoints: {org_endpoints['total']}")

for method, count in org_endpoints['by_method'].items():
    print(f"  {method}: {count} endpoints")
```

### Example 5: Compare Operations Across Vendors

```python
from api_validator import NetworkDeviceValidator

validator = NetworkDeviceValidator()

# Compare same operation across vendors
comparison = validator.compare_vendors("firewall")
print(f"Firewall operation available in: {comparison['available_in']}")
```

### Example 6: Generate Device API Client

```python
from code_generator import CodeGenerator

gen = CodeGenerator()

# Generate FortiGate client
gen.generate_fndn_client("fortigate", "fortigate_client.py")

# Generate Meraki client
gen.generate_meraki_client("organizations", "meraki_org_client.py")

# Generate validation code
gen.generate_endpoint_validation("device_validators.py")
```

## Integration with Network Observability Features

### Device Discovery

When discovering devices:
```python
from api_validator import FortiGateAPIValidator, MerakiAPIValidator

fg_validator = FortiGateAPIValidator()
meraki_validator = MerakiAPIValidator()

# Validate FortiGate discovery capabilities
fg_stats = fg_validator.get_statistics()
print(f"FortiGate supports {fg_stats['total_endpoints']} operations")

# Validate Meraki API access
meraki_stats = meraki_validator.get_statistics()
print(f"Meraki supports {meraki_stats['meraki']['total_endpoints']} endpoints")
```

### Device Management

When managing devices:
```python
from api_validator import NetworkDeviceValidator

device_validator = NetworkDeviceValidator()

# Validate operation for device type
def execute_device_operation(device):
    operation = "firewall"
    is_valid, desc = device_validator.validate_device_operation(device.vendor, operation)

    if is_valid:
        return device.execute(operation)
    else:
        raise ValueError(f"{device.vendor} doesn't support {operation}")
```

### Topology Visualization

When displaying available operations:
```python
from api_validator import NetworkDeviceValidator

device_validator = NetworkDeviceValidator()

# Get operations available for each vendor
vendors = ["fortigate", "meraki"]
available_ops = {}

for vendor in vendors:
    caps = device_validator.get_vendor_capabilities(vendor)
    available_ops[vendor] = caps.get('total_endpoints', 0)

# Display in topology visualization
print(f"FortiGate: {available_ops['fortigate']} operations available")
print(f"Meraki: {available_ops['meraki']} endpoints available")
```

## Testing Integration

### Test 1: MCP Client Connection

```bash
python3 << 'EOF'
from mcp_client import MCPClient

client = MCPClient.from_env()
stats = client.get_statistics()
print(f"Connected! Meraki: {stats['meraki']['total_endpoints']}, FNDN: {stats['fndn']['total_endpoints']}")
EOF
```

### Test 2: Device Operation Validation

```bash
python3 << 'EOF'
from api_validator import FortiGateAPIValidator

validator = FortiGateAPIValidator()
is_valid, info = validator.validate_endpoint("firewall")
print(f"FortiGate firewall operation: {is_valid}")
EOF
```

### Test 3: Meraki Endpoint Validation

```bash
python3 << 'EOF'
from api_validator import MerakiAPIValidator

validator = MerakiAPIValidator()
is_valid, summary = validator.validate_endpoint(
    "/organizations/{organizationId}/networks",
    "GET"
)
print(f"Meraki endpoint valid: {is_valid}")
EOF
```

### Test 4: API Endpoint from FastAPI

```bash
# Check MCP status through API
curl http://localhost:8000/mcp/status

# Should return:
# {
#   "status": "available",
#   "meraki_endpoints": 862,
#   "fndn_endpoints": 814,
#   "total_endpoints": 1676,
#   "endpoints": {...}
# }
```

### Test 5: Code Generation

```bash
python3 << 'EOF'
from code_generator import CodeGenerator

gen = CodeGenerator()
gen.generate_meraki_client("organizations", "test_client.py")
print("Generated test_client.py")
EOF
```

## AI Tool Configuration

### Claude Desktop
✅ Already configured in `~/.config/Claude/claude_desktop_config.json`

### Cline
Follow Step 6 above to configure `.cline/mcp.json`

### Cursor
Add to `.cursor/settings.json`:
```json
{
  "mcp": {
    "servers": [
      {
        "name": "FNDN & Meraki API",
        "command": "python3",
        "args": ["/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/mcp_server.py"]
      }
    ]
  }
}
```

### Ralph Autonomous Agent
Add to @fix_plan.md automation:
```markdown
- [ ] Validate all device operations using MCP before deployment
- [ ] Use code_generator.py to generate device client code
- [ ] Check operation availability with api_validator.py
```

### Antigravity IDE
Add to AGENTS.md rules:
```markdown
**MCP Integration Rule**: All device operations MUST be validated through api_validator before implementation
```

## File Structure

```
network-observability-platform/
├── app/
│   ├── main.py                          (Updated with MCP client)
│   └── api/
│       └── ai_assistant.py
│
├── mcp_client.py                        (NEW - Copy from fndn module)
├── code_generator.py                    (NEW - Copy from fndn module)
├── api_validator.py                     (NEW - Network observability specific)
├── .env.template                        (NEW - Configuration template)
│
├── MCP_INTEGRATION_SETUP.md             (This file)
├── NETWORK_OBSERVABILITY_MCP_QUICK_START.md (Quick start guide)
│
├── AGENTS.md                            (Update with MCP rules)
├── README.md                            (Update with MCP info)
│
└── docs/
    └── MCP_INTEGRATION.md               (Optional - Advanced guide)
```

## Key Features Enabled

| Feature | Tool | Capability |
|---------|------|-----------|
| **Search Operations** | Claude/Cline | Find FortiGate operations by keyword |
| **Validate Before Deploy** | Ralph/Antigravity | Check operations exist |
| **Generate Code** | Cursor/Claude | Auto-create device API clients |
| **Get Details** | All | View operation specs |
| **Statistics** | Dashboard | Show API coverage |
| **Compare Vendors** | AI Agents | Find equivalent operations |
| **Device Management** | Platform | Validate device operations |

## Configuration Environment Variables

```bash
# MCP Server (Required for integration)
MCP_HOST=127.0.0.1
MCP_PORT=11503

# FortiGate Live API (Optional)
FORTIGATE_HOST=192.168.1.1
FORTIGATE_USERNAME=admin
FORTIGATE_PASSWORD=admin

# Meraki Live API (Optional)
MERAKI_API_KEY=your_key
MERAKI_ORG_ID=org_id

# Fortinet Manager (Optional - if adding FortiManager integration)
FORTIMANAGER_HOST=192.168.0.1
FORTIMANAGER_USERNAME=admin
FORTIMANAGER_PASSWORD=admin
```

## Next Steps

1. ✅ Copy integration files (Step 1)
2. ✅ Configure .env (Step 2)
3. ✅ Verify MCP client in main.py (Step 3)
4. ✅ Create api_validator.py (Step 4)
5. ✅ Verify Claude Desktop config (Step 5)
6. ✅ Configure other AI tools (Steps 6-7)
7. ✅ Run integration tests
8. **Add API validation to device management code**
9. **Test with Claude/Cline/Antigravity**
10. **Commit changes to git**

## Troubleshooting

### MCP Server Not Found
```bash
# Check if MCP server is running
python3 /media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/mcp_server.py

# Or check if port is in use
lsof -i :11503
```

### Import Errors
```bash
# Make sure sys.path includes fndn module
export PYTHONPATH="${PYTHONPATH}:/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn"
```

### Claude Desktop Not Recognizing MCP
```bash
# Restart Claude Desktop after configuration changes
# Check configuration
cat ~/.config/Claude/claude_desktop_config.json
```

## Support

- **MCP Server Docs:** `/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/README_MCP.md`
- **Quick Start:** `NETWORK_OBSERVABILITY_MCP_QUICK_START.md`
- **API Validator:** `api_validator.py` (docstrings)
- **Code Generator:** `code_generator.py` (docstrings)

## Statistics

- **Total Endpoints Available:** 1,676
  - FNDN (Fortinet): 814 (FortiGate: 465, FortiManager: 92, FortiAnalyzer: 257)
  - Meraki: 862 (GET: 468, POST: 157, PUT: 174, DELETE: 63)
- **Offline:** All documentation available without internet
- **Zero Dependencies:** Uses only Python stdlib

---

**Ready to integrate!** Follow the setup steps above to enable MCP server access in device management code and all AI tools.
