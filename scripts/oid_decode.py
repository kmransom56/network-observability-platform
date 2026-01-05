#!/usr/bin/env python3
"""
OID Decoder Script for NeDi Integration

This script can be called from PHP to decode OID-based device names.
It uses free OID lookup services (no API key required).

Usage from PHP:
    $decoded = shell_exec("python3 /path/to/oid_decode.py " . 
                          escapeshellarg($oid_string) . " " . 
                          escapeshellarg($device_type));
    
Usage from command line:
    python3 oid_decode.py <oid_string> [device_type]
    python3 oid_decode.py 1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51 FortiAP
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from reusable.oid_lookup import OIDLookup, decode_device_oid


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python3 oid_decode.py <oid_string> [device_type]")
        print("Example: python3 oid_decode.py 1.16.70.80.50.51.49 FortiAP")
        sys.exit(1)
    
    oid_string = sys.argv[1]
    device_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Initialize lookup with caching
    # Cache file location (optional - can be shared across calls)
    cache_file = os.path.join(os.path.expanduser("~"), ".oid_lookup_cache.json")
    cache = {}
    
    # Try to load cache if it exists
    if os.path.exists(cache_file):
        try:
            import json
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        except:
            pass
    
    lookup = OIDLookup(cache=cache)
    
    # If device_type is provided, use device OID decoding
    if device_type:
        try:
            decoded = decode_device_oid(oid_string, device_type)
            print(decoded)
            
            # Save cache
            try:
                import json
                with open(cache_file, 'w') as f:
                    json.dump(cache, f)
            except:
                pass
            
            sys.exit(0)
        except Exception as e:
            # Fallback to basic lookup
            pass
    
    # Try standard OID lookup
    try:
        result = lookup.lookup(oid_string)
        if result and result.get('name'):
            print(result['name'])
            
            # Save cache
            try:
                import json
                with open(cache_file, 'w') as f:
                    json.dump(cache, f)
            except:
                pass
            
            sys.exit(0)
    except Exception as e:
        pass
    
    # If all else fails, return original
    if device_type:
        print(f"{device_type}-{oid_string}")
    else:
        print(oid_string)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
