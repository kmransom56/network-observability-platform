# OidView MIB API Integration

This document describes how to use the OidView MIB API for SNMP MIB object lookup and OID decoding in the Network Observability Platform.

## Overview

The [OidView MIB API](https://www.oidview.com/api/api.html) provides programmatic access to thousands of SNMP MIBs, allowing you to:

- Look up MIB object information by OID or name
- Get vendor and MIB information
- Search MIB objects across vendors
- Decode OIDs to human-readable names and descriptions

## API Client

The platform includes a Python client for the OidView API located at `reusable/oidview_client.py`.

### Installation

No additional dependencies are required beyond the standard `requests` library (already in `requirements.txt`).

### Getting an API Key

1. Visit https://www.oidview.com/api/api.html
2. Sign up for an API account
3. Obtain your API key
4. Set it as an environment variable:

```bash
export OIDVIEW_API_KEY='your-api-key-here'
```

Or pass it directly to the client:

```python
from reusable.oidview_client import OidViewClient

client = OidViewClient(api_key="your-api-key")
```

## Usage Examples

### Basic Usage

```python
from reusable.oidview_client import OidViewClient

# Initialize client
client = OidViewClient(api_key="your-api-key")

# Get MIB object info by OID
result = client.get_mib_object_info(oid="1.3.6.1.2.1.1.1.0")
print(result)

# Get MIB object info by name
result = client.get_mib_object_info_by_name(
    name="sysDescr", 
    vendor="RFC1213"
)
print(result)
```

### Decoding OIDs

```python
# Decode OID to MIB object name
name = client.decode_oid_to_name("1.3.6.1.2.1.1.1.0")
print(f"Name: {name}")

# Get OID description
description = client.get_oid_description("1.3.6.1.2.1.1.1.0")
print(f"Description: {description}")
```

### Vendor Information

```python
# Get all vendors
vendors = client.get_vendors()

# Get vendor info
vendor_info = client.get_vendor_info(vendor="Fortinet")

# Get vendor MIBs
mibs = client.get_vendor_mibs(vendor="Fortinet")
```

### Searching MIB Objects

```python
# Search for MIB objects in a vendor's MIBs
results = client.search_mib_objects_by_vendor(
    vendor="Fortinet",
    token="system"
)
```

## Available API Methods

| Method | Description |
|--------|-------------|
| `get_vendors()` | List all vendors with MIBs |
| `get_vendor_info(vendor)` | Get vendor information |
| `get_vendor_mibs(vendor)` | Get all MIBs for a vendor |
| `get_mib_info(mib)` | Get detailed MIB information |
| `get_mib_object_info(oid)` | Get MIB object info by OID |
| `get_mib_object_info_by_name(name, vendor, mib)` | Get MIB object info by name |
| `get_mib_object_parent(oid)` | Get parent MIB object |
| `get_mib_object_path(oid)` | Get complete OID path |
| `get_mib_object_children(oid)` | Get child MIB objects |
| `get_mib_object_siblings(oid)` | Get sibling MIB objects |
| `get_mib_object_child_count(oid)` | Get child count |
| `get_mib_object_sibling_count(oid)` | Get sibling count |
| `search_mib_objects_by_vendor(vendor, token)` | Search MIB objects |
| `decode_oid_to_name(oid)` | Convenience method to decode OID |
| `get_oid_description(oid)` | Get OID description |

## Integration with NeDi OID Decoding

The OidView API can enhance the existing OID decoding functionality in NeDi. Here's how to integrate it:

### Enhanced OID Decoding Function

You can enhance the `DecodeOIDDeviceName` function in `/var/nedi/html/inc/libdev.php` to use the OidView API for better OID resolution:

```php
function DecodeOIDDeviceName($neighbor, $link) {
    global $dev;
    
    // Existing OID pattern matching
    if( preg_match("/^(FortiAP|FortiSwitch|FortiGate)-(\\d+\\.\\d+.*)$/", $neighbor, $matches) ){
        $device_type = $matches[1];
        $oid_string = $matches[2];
        
        // Try database lookup first (existing logic)
        // ...
        
        // If not found, could call Python script that uses OidView API
        // $decoded = shell_exec("python3 /path/to/oidview_decode.py " . escapeshellarg($oid_string));
        
        // Fallback to ASCII decoding (existing logic)
        // ...
    }
    
    return $neighbor;
}
```

### Python Integration Script

Create a Python script that can be called from PHP:

```python
#!/usr/bin/env python3
"""OID decoder using OidView API - called from PHP"""

import sys
import os
from pathlib import Path

# Add reusable to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'reusable'))

from reusable.oidview_client import OidViewClient

def decode_oid(oid_string):
    """Decode OID string using OidView API."""
    api_key = os.getenv('OIDVIEW_API_KEY')
    if not api_key:
        return None
    
    client = OidViewClient(api_key=api_key)
    
    # Try to get MIB object info
    try:
        result = client.get_mib_object_info(oid=oid_string)
        if result and 'name' in result:
            return result['name']
    except:
        pass
    
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        oid = sys.argv[1]
        decoded = decode_oid(oid)
        if decoded:
            print(decoded)
```

## Response Formats

The API supports both JSON and XML response formats. By default, the client requests JSON. To get XML:

```python
result = client.get_mib_object_info(oid="1.3.6.1.2.1.1.1.0", format='xml')
```

## Error Handling

The client raises exceptions for API errors. Always wrap API calls in try-except blocks:

```python
try:
    result = client.get_mib_object_info(oid="1.3.6.1.2.1.1.1.0")
except Exception as e:
    print(f"API error: {e}")
    # Fallback to local decoding
```

## Rate Limiting

Be aware that the OidView API may have rate limits. Consider:

- Caching API responses
- Using local MIB files when possible
- Implementing request throttling
- Using the API as a fallback when local decoding fails

## Example: Complete OID Decoding Workflow

```python
from reusable.oidview_client import OidViewClient
import os

def decode_device_oid(oid_string, device_type="FortiAP"):
    """
    Decode OID-based device name with fallback strategy.
    
    1. Try OidView API
    2. Try database lookup
    3. Try ASCII decoding
    4. Return original
    """
    api_key = os.getenv('OIDVIEW_API_KEY')
    
    # Step 1: Try OidView API
    if api_key:
        try:
            client = OidViewClient(api_key=api_key)
            result = client.get_mib_object_info(oid=oid_string)
            if result and 'name' in result:
                return f"{device_type}-{result['name']}"
        except:
            pass
    
    # Step 2: Try database lookup (existing logic)
    # ...
    
    # Step 3: ASCII decoding (existing logic)
    decoded = ""
    for part in oid_string.split("."):
        if part.isdigit():
            num = int(part)
            if 32 <= num <= 126:
                decoded += chr(num)
    
    if decoded:
        return f"{device_type}-{decoded}"
    
    # Step 4: Return original
    return f"{device_type}-{oid_string}"
```

## Testing

Run the example script to test the API:

```bash
# Set API key
export OIDVIEW_API_KEY='your-api-key'

# Run examples
python reusable/examples/oidview_usage.py
```

## References

- [OidView MIB API Documentation](https://www.oidview.com/api/api.html)
- [API Client Source Code](../reusable/oidview_client.py)
- [Usage Examples](../reusable/examples/oidview_usage.py)
