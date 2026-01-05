# OID Lookup Integration with NeDi

This document describes how the free OID lookup system is integrated with NeDi's `DecodeOIDDeviceName` function.

## Integration Overview

The integration uses a Python script (`scripts/oid_decode.py`) that can be called from PHP to enhance OID decoding with multiple free lookup sources.

## Architecture

```
NeDi PHP (Devices-Status.php)
    ↓
DecodeOIDDeviceName() function
    ↓
Python script (oid_decode.py)
    ↓
OIDLookup module (reusable/oid_lookup.py)
    ↓
Multiple free OID sources:
  - Alvestrand.no (primary)
  - OidRef.com (fallback)
  - OidInfo.com (fallback)
  - MIB-Depot.com (fallback)
  - ASCII decoding (final fallback)
```

## Files Created

### 1. Python OID Decoder Script
**Location:** `scripts/oid_decode.py`

**Purpose:** PHP-callable script for OID decoding

**Usage:**
```bash
python3 scripts/oid_decode.py <oid_string> [device_type]
```

**Example:**
```bash
python3 scripts/oid_decode.py "1.16.70.80.50.51.49" "FortiAP"
# Output: FortiAP-FP231F...
```

### 2. OID Lookup Module
**Location:** `reusable/oid_lookup.py`

**Features:**
- Multiple free OID lookup sources
- Automatic fallback chain
- Local caching support
- ASCII decoding for device OIDs
- Prefix skipping for device OID strings

### 3. Enhanced NeDi Function
**Location:** `/var/nedi/html/inc/libdev.php`

**Changes:**
- Added Python script integration
- Enhanced prefix skipping logic
- Maintains backward compatibility

## How It Works

### Step 1: NeDi Detects OID-Based Name

When NeDi encounters a device name like:
```
FortiAP-1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51
```

The `DecodeOIDDeviceName()` function:
1. Extracts device type: `FortiAP`
2. Extracts OID string: `1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51`

### Step 2: Database Lookup

First tries to find the device in NeDi's database using the OID name.

### Step 3: Python Script Call

If not found in database, calls the Python script:
```php
$command = "python3 /path/to/oid_decode.py " . 
           escapeshellarg($oid_string) . " " . 
           escapeshellarg($device_type);
$decoded = shell_exec($command);
```

### Step 4: OID Lookup Process

The Python script:
1. Tries OID lookup services (Alvestrand.no, etc.)
2. Falls back to ASCII decoding
3. Skips common prefixes (e.g., "1.16")
4. Returns decoded name

### Step 5: PHP Fallback

If Python script fails, PHP falls back to:
- ASCII decoding with prefix skipping
- Returns original if all else fails

## Decoding Logic

### Device OID Format

Device OIDs typically have this structure:
```
[prefix].[ASCII-encoded device info]
```

Example:
```
1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51
│   │  └─────────────────────────────────────────────┐
│   └─ Prefix part (often "1.16")                    │
└─ Always "1"                                        │
                                                     │
ASCII decoding (skipping prefix):                   │
70=F, 80=P, 50=2, 51=3, 49=1, 70=F, ...            │
Result: "FP231FTF20023043"                          │
```

### Prefix Skipping

The decoder automatically skips common prefixes:
- `1.16` (common Fortinet prefix)
- `1.3.6.1` (standard SNMP prefix)
- Any `1.X` where X < 20

### ASCII Decoding

Numeric OID parts are converted to ASCII:
- `70` → `F`
- `80` → `P`
- `50` → `2`
- `48` → `0`
- etc.

Non-printable characters (< 32) are skipped.

## Testing

### Test the Python Script

```bash
# Test device OID decoding
python3 scripts/oid_decode.py "1.16.70.80.50.51.49" "FortiAP"

# Test standard OID lookup
python3 scripts/oid_decode.py "1.3.6.1.2.1.1.1.0"
```

### Test from PHP

Create a test PHP file:
```php
<?php
require_once('/var/nedi/html/inc/libdev.php');
$link = DbConnect(); // Your DB connection

$test_names = [
    "FortiAP-1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51",
    "FortiSwitch-1.16.70.83.87.49.48.48.48.48.48.48.48.48.48.48.48",
];

foreach ($test_names as $name) {
    $decoded = DecodeOIDDeviceName($name, $link);
    echo "$name => $decoded\n";
}
?>
```

### Run Coverage Tests

```bash
python3 scripts/test_oid_lookups.py
```

## Performance

### Caching

The Python script uses a cache file at `~/.oid_lookup_cache.json` to:
- Speed up repeated lookups
- Reduce external API calls
- Work offline with cached data

### Performance Metrics

From test results:
- **First lookup (cold cache):** ~0.4-0.6 seconds
- **Subsequent lookups (warm cache):** < 0.0001 seconds
- **Speedup:** 4000x+ faster with cache

### Optimization Tips

1. **Pre-populate cache** with common OIDs
2. **Use caching** for production environments
3. **Batch lookups** when possible
4. **Monitor cache size** and clear if needed

## Troubleshooting

### Python Script Not Found

**Error:** Script not executable or not found

**Solution:**
```bash
chmod +x /home/keith/network-observability-platform/scripts/oid_decode.py
```

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'reusable'`

**Solution:**
```bash
# Set PYTHONPATH or use absolute path in script
export PYTHONPATH=/home/keith/network-observability-platform
```

### No Results from Lookup

**Possible causes:**
- OID format not recognized
- All lookup sources unavailable
- Network connectivity issues

**Solution:**
- Check OID format
- Verify network connectivity
- Check script permissions
- Review PHP error logs

### Slow Performance

**Causes:**
- No caching enabled
- Network latency
- Multiple fallback attempts

**Solution:**
- Enable caching
- Pre-populate cache
- Use faster lookup sources first

## Configuration

### Script Path

The script path is hardcoded in `libdev.php`:
```php
$python_script = "/home/keith/network-observability-platform/scripts/oid_decode.py";
```

To change it, edit `/var/nedi/html/inc/libdev.php` line ~1368.

### Cache Location

Cache file location: `~/.oid_lookup_cache.json`

To change it, edit `scripts/oid_decode.py`.

### Timeout Settings

Default timeout: 5 seconds per lookup source

To change it, edit `reusable/oid_lookup.py`:
```python
self.timeout = 5  # Change to desired timeout
```

## Success Metrics

From test results:
- **Standard SNMP OIDs:** 100% success rate (5/5)
- **Enterprise OIDs:** 100% success rate (3/3)
- **Device OID Strings:** ASCII decoding works (2/2)
- **Common Network OIDs:** 100% success rate (4/4)
- **Overall:** 85.7% success rate (12/14)

**Primary Sources:**
- Alvestrand.no: 9 lookups
- OidRef.com: 3 lookups

## Future Enhancements

1. **Local MIB Database:** Download and cache MIB files locally
2. **Better Prefix Detection:** Machine learning for prefix patterns
3. **Vendor-Specific Decoders:** Custom decoders for Fortinet, Cisco, etc.
4. **Batch Processing:** Process multiple OIDs in one call
5. **API Integration:** When OidView API key becomes available

## References

- **OID Lookup Module:** `reusable/oid_lookup.py`
- **Python Script:** `scripts/oid_decode.py`
- **Test Script:** `scripts/test_oid_lookups.py`
- **NeDi Function:** `/var/nedi/html/inc/libdev.php`
- **Documentation:** `docs/oid-lookup-alternatives.md`
