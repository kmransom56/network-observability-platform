# Network Observability Platform - MCP Quick Start

**Fast integration guide for using MCP server with Network Observability Platform**

## 1️⃣ Copy Files (2 minutes)

```bash
cd /home/keith/network-observability-platform

# Files are already in place:
# - mcp_client.py (copied)
# - code_generator.py (copied)
# - api_validator.py (created - custom for network observability)
# - .env.template (copied)
```

## 2️⃣ Install MCP Client in Main Application

MCP client is already initialized in `app/main.py`:

```python
try:
    from mcp_client import MCPClient
    mcp_client = MCPClient.from_env()
    logger.info(f"MCP Server: {mcp_stats['meraki']['total_endpoints']} Meraki endpoints available")
except Exception as e:
    logger.warning(f"MCP Server initialization: {e}")
    mcp_client = None
```

## 3️⃣ Use in Your Code

### Validate FortiGate Operations

```python
from api_validator import FortiGateAPIValidator

validator = FortiGateAPIValidator()

# Validate before executing FortiGate API call
is_valid, description = validator.validate_endpoint("firewall")
if is_valid:
    # Safe to use FortiGate API
    pass
else:
    logger.error("FortiGate endpoint not found in API docs")
```

### Validate Meraki Endpoints

```python
from api_validator import MerakiAPIValidator

validator = MerakiAPIValidator()

# Before making Meraki API call
is_valid, summary = validator.validate_endpoint(
    "/organizations/{organizationId}/networks",
    "GET"
)

if is_valid:
    # Safe to proceed
    pass
```

### Validate Across Vendors

```python
from api_validator import NetworkDeviceValidator

device_validator = NetworkDeviceValidator()

# Compare operation availability across vendors
comparison = device_validator.compare_vendors("firewall")
print(f"Available in: {comparison['available_in']}")  # ['fortigate', 'meraki']

# Validate device operation
is_valid, desc = device_validator.validate_device_operation(
    vendor="fortigate",
    operation="firewall"
)
```

### Search for Operations

```python
from api_validator import FortiGateAPIValidator, MerakiAPIValidator

# Search FortiGate operations
fg_validator = FortiGateAPIValidator()
firewall_ops = fg_validator.get_endpoint_info("firewall")
print(f"Found {firewall_ops['total_results']} firewall operations")

# Search Meraki endpoints
meraki_validator = MerakiAPIValidator()
device_endpoints = meraki_validator.get_endpoint_info("device")
print(f"Found {device_endpoints['total_results']} device endpoints")
```

## 4️⃣ Test It Works

```bash
# Test 1: Check MCP status via API
curl http://localhost:8000/mcp/status

# Test 2: Validate FortiGate operation
python3 -c "
from api_validator import FortiGateAPIValidator
v = FortiGateAPIValidator()
valid, desc = v.validate_endpoint('firewall')
print(f'FortiGate firewall operation valid: {valid}')
"

# Test 3: Validate Meraki endpoint
python3 -c "
from api_validator import MerakiAPIValidator
v = MerakiAPIValidator()
valid, desc = v.validate_endpoint('/organizations/{organizationId}/networks', 'GET')
print(f'Meraki endpoint valid: {valid}')
"

# Test 4: Search operations
python3 -c "
from api_validator import FortiGateAPIValidator
v = FortiGateAPIValidator()
results = v.get_endpoint_info('firewall')
print(f'Found {results.get(\"total_results\", 0)} firewall operations')
"
```

## 5️⃣ Use with AI Tools

### Claude Desktop
When developing with Claude:
- Already configured ✓
- Ask for FortiGate/Meraki API help
- Claude has access to real endpoints
- Restart Claude Desktop to refresh

### Cline Agent
MCP server is available for Cline workflows:
```python
# Cline can now validate device operations
from api_validator import NetworkDeviceValidator
validator = NetworkDeviceValidator()
# Cline uses this for validation
```

### Ralph Autonomous Agent
Add to automation scripts:
```python
from api_validator import FortiGateAPIValidator

def validate_fortigate_deployment(operations):
    validator = FortiGateAPIValidator()
    for operation in operations:
        is_valid, _ = validator.validate_endpoint(operation)
        if not is_valid:
            raise ValueError(f"Invalid operation: {operation}")
```

### Antigravity IDE
Use in agent rules:
```python
# Validate all FortiGate/Meraki operations before execution
from api_validator import NetworkDeviceValidator
validator = NetworkDeviceValidator()
# Use validator in AI-generated code
```

## 📊 What You Get

| Feature | Benefit |
|---------|---------|
| **862 Meraki Endpoints** | Complete API documentation offline |
| **465 FortiGate Operations** | Full Fortinet API documentation |
| **Search Capability** | Find endpoints by keyword |
| **Validation** | Ensure operations exist before use |
| **Code Generation** | Auto-generate API clients |
| **AI Integration** | Claude, Cline, Cursor all have MCP access |
| **Device Comparison** | Compare operations across vendors |

## 🔧 Configuration

### .env.template File

```bash
# MCP Server (required)
MCP_HOST=127.0.0.1
MCP_PORT=11503

# Meraki API (optional - for live API)
MERAKI_API_KEY=your_key
MERAKI_ORG_ID=your_org_id

# FortiGate (optional - for live API)
FORTIGATE_HOST=192.168.1.1
FORTIGATE_USERNAME=admin
FORTIGATE_PASSWORD=admin
```

Load in code:
```python
import os
from dotenv import load_dotenv
load_dotenv('.env.template')

mcp_host = os.getenv('MCP_HOST')
mcp_port = os.getenv('MCP_PORT')
```

## 📚 Common Tasks

### Task 1: Validate Device Operations

```python
from api_validator import NetworkDeviceValidator

validator = NetworkDeviceValidator()

operations = [
    ("fortigate", "firewall"),
    ("fortigate", "system"),
    ("meraki", "/organizations/{organizationId}/networks"),
]

for vendor, op in operations:
    is_valid, desc = validator.validate_device_operation(vendor, op)
    print(f"{vendor}/{op}: {is_valid}")
```

### Task 2: Get Available Operations for a Vendor

```python
from api_validator import FortiGateAPIValidator

validator = FortiGateAPIValidator()
stats = validator.get_statistics()
print(f"Total FortiGate operations: {stats['total_endpoints']}")

# Get operations by resource type
firewall_ops = validator.get_endpoints_by_resource("firewall")
print(f"Firewall operations: {firewall_ops['total']}")
```

### Task 3: Search Across Vendors

```python
from api_validator import NetworkDeviceValidator

device_validator = NetworkDeviceValidator()

# Find "firewall" in both vendors
fg_results = device_validator.fortigate.get_endpoint_info("firewall")
meraki_results = device_validator.meraki.get_endpoint_info("firewall")

print(f"FortiGate firewall operations: {fg_results['total_results']}")
print(f"Meraki firewall endpoints: {meraki_results['total_results']}")
```

### Task 4: Generate Device-Specific Code

```python
from code_generator import CodeGenerator

gen = CodeGenerator()

# Generate FortiGate client
gen.generate_fndn_client("fortigate", "fortigate_client.py")

# Generate Meraki client
gen.generate_meraki_client("organizations", "meraki_client.py")

# Generate validation code
gen.generate_endpoint_validation("validators.py")
```

## 🐛 Troubleshooting

### "MCP client not available"

**Problem:** Can't connect to MCP server

**Solution:**
```bash
# 1. Check MCP server is running
python3 /media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/mcp_server.py &

# 2. Check .env configuration
cat .env.template

# 3. Verify port is accessible
nc -zv 127.0.0.1 11503
```

### "ModuleNotFoundError: No module named 'api_validator'"

**Problem:** Can't find api_validator.py

**Solution:**
```python
# Add to your code
import sys
sys.path.insert(0, '/home/keith/network-observability-platform')
from api_validator import NetworkDeviceValidator
```

### "Endpoint not found"

**Problem:** Validation says endpoint doesn't exist

**Solution:**
```bash
# Search for similar operations
python3 -c "
from api_validator import FortiGateAPIValidator
v = FortiGateAPIValidator()
results = v.get_endpoint_info('firewall')
for r in results.get('endpoints', []):
    print(r)
"
```

## 📖 Full Documentation

For detailed information, see:
- **Integration Guide:** `MCP_INTEGRATION_SETUP.md`
- **MCP Server Docs:** `/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn/README_MCP.md`
- **API Validator:** `api_validator.py` (docstrings)
- **Code Generator:** `code_generator.py` (docstrings)

## ✅ Verification Checklist

- [ ] Copied mcp_client.py
- [ ] Copied code_generator.py
- [ ] Created api_validator.py
- [ ] Updated main.py with MCP client
- [ ] Created .env with configuration
- [ ] Ran Test 1 (MCP status)
- [ ] Ran Test 2 (FortiGate validation)
- [ ] Ran Test 3 (Meraki validation)
- [ ] Ran Test 4 (search operations)
- [ ] Tested with Claude/Cline/Antigravity
- [ ] Integrated validators into device management code

## 🚀 Next Steps

1. **Start using MCP** in device management code
2. **Validate operations** before API calls
3. **Generate code** for new device integrations
4. **Ask Claude** for API help (it now has accurate data!)

---

**You're all set!** MCP is now integrated with the Network Observability Platform. 🎉

**Questions?** Check the troubleshooting section or review the full integration guide.
