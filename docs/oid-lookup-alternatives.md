# OID Lookup Alternatives (No API Key Required)

Since the OidView API key registration page may not be working, this document describes free alternatives for OID lookup that don't require API keys.

## Available Solutions

### 1. **OIDLookup Module** (Recommended)

The `reusable.oid_lookup` module provides free OID lookups using multiple public sources:

**Features:**
- ✅ No API key required
- ✅ Multiple fallback sources
- ✅ Local caching support
- ✅ ASCII decoding for device OIDs
- ✅ Works offline with cached data

**Usage:**

```python
from reusable.oid_lookup import OIDLookup, decode_device_oid

# Initialize lookup
lookup = OIDLookup()

# Look up standard SNMP OID
result = lookup.lookup("1.3.6.1.2.1.1.1.0")
print(result)
# {'name': 'sysDescr', 'description': '...', 'source': 'alvestrand.no'}

# Get just the name
name = lookup.get_name("1.3.6.1.2.1.1.1.0")
print(name)  # "sysDescr"

# Decode device OID strings
decoded = decode_device_oid("1.16.70.80.50.51.49", "FortiAP")
print(decoded)  # "FortiAP-FP231F..."
```

**Supported Sources:**
1. **Alvestrand.no** - Reliable, works well for standard SNMP OIDs
2. **OidRef.com** - HTML-based lookup (if available)
3. **OidInfo.com** - Alternative source (if available)
4. **ASCII Decoding** - Fallback for device name OIDs

### 2. **Alvestrand.no** (Direct)

Direct access to the Alvestrand OID registry:

- **URL Format:** `https://www.alvestrand.no/objectid/{oid}.html`
- **Example:** https://www.alvestrand.no/objectid/1.3.6.1.2.1.1.1.0.html
- **Status:** ✅ Working
- **No API Key Required**

### 3. **OidView API** (If Registration Works)

If the OidView API key registration page starts working:

- **Registration:** https://www.oidview.com/contact.html
- **API Docs:** https://www.oidview.com/api/api.html
- **Client:** `reusable.oidview_client.OidViewClient`

## Integration with NeDi

### Option 1: Use OIDLookup in PHP

Create a Python script that can be called from PHP:

```python
#!/usr/bin/env python3
"""OID decoder - called from PHP"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'reusable'))

from reusable.oid_lookup import OIDLookup, decode_device_oid

if __name__ == "__main__":
    if len(sys.argv) > 2:
        oid = sys.argv[1]
        device_type = sys.argv[2]
        result = decode_device_oid(oid, device_type)
        print(result)
    elif len(sys.argv) > 1:
        oid = sys.argv[1]
        lookup = OIDLookup()
        result = lookup.get_name(oid)
        if result:
            print(result)
```

Then call from PHP:

```php
function DecodeOIDDeviceName($neighbor, $link) {
    // ... existing code ...
    
    // Try Python OID lookup
    $decoded = shell_exec("python3 /path/to/oid_decode.py " . 
                          escapeshellarg($oid_string) . " " . 
                          escapeshellarg($device_type));
    if ($decoded) {
        return trim($decoded);
    }
    
    // Fallback to existing logic
    // ...
}
```

### Option 2: Direct ASCII Decoding (Current Implementation)

The current `DecodeOIDDeviceName` function in NeDi already does ASCII decoding, which works well for device names like:

- `FortiAP-1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51`
- Decodes to: `FortiAP-FP231F-20035593`

This is sufficient for most device name decoding needs.

## Comparison

| Solution | API Key | Reliability | Speed | Caching |
|----------|---------|-------------|-------|---------|
| OIDLookup | ❌ No | ✅ High | ⚡ Fast (with cache) | ✅ Yes |
| Alvestrand.no | ❌ No | ✅ High | ⚡ Fast | ❌ No |
| OidView API | ✅ Yes | ⚠️ Unknown | ⚡ Fast | ❌ No |
| ASCII Decode | ❌ No | ✅ High | ⚡ Very Fast | N/A |

## Recommendations

1. **For Device Name Decoding:** Use the existing ASCII decoding (already implemented in NeDi)
2. **For Standard SNMP OIDs:** Use `OIDLookup` module with Alvestrand.no as primary source
3. **For Production:** Implement caching to reduce external API calls
4. **For Offline Use:** Pre-populate cache with common OIDs

## Example: Complete Integration

```python
from reusable.oid_lookup import OIDLookup, decode_device_oid

def decode_neighbor_name(neighbor_name, device_type="FortiAP"):
    """
    Decode neighbor device name with multiple fallback strategies.
    
    Handles formats like:
    - FortiAP-1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51
    - Standard OIDs: 1.3.6.1.2.1.1.1.0
    """
    # Check if it's a device OID format
    if re.match(r'^(FortiAP|FortiSwitch|FortiGate)-(\d+\.\d+.*)$', neighbor_name):
        match = re.match(r'^(FortiAP|FortiSwitch|FortiGate)-(\d+\.\d+.*)$', neighbor_name)
        device_type = match.group(1)
        oid_string = match.group(2)
        
        # Try OID lookup first
        lookup = OIDLookup()
        result = lookup.lookup(oid_string)
        if result and result.get('name'):
            return f"{device_type}-{result['name']}"
        
        # Fallback to ASCII decoding
        decoded = decode_device_oid(oid_string, device_type)
        return decoded
    
    # For standard OIDs, try lookup
    lookup = OIDLookup()
    result = lookup.lookup(neighbor_name)
    if result:
        return result.get('name', neighbor_name)
    
    return neighbor_name
```

## Testing

Test the OID lookup:

```bash
# Run examples
python reusable/examples/oid_lookup_usage.py

# Test specific OID
python3 -c "
from reusable.oid_lookup import OIDLookup
lookup = OIDLookup()
result = lookup.lookup('1.3.6.1.2.1.1.1.0')
print(result)
"
```

## References

- **OIDLookup Module:** `reusable/oid_lookup.py`
- **Usage Examples:** `reusable/examples/oid_lookup_usage.py`
- **Alvestrand OID Registry:** https://www.alvestrand.no/objectid/
- **OidView API (if working):** https://www.oidview.com/api/api.html
