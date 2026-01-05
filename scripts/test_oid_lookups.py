#!/usr/bin/env python3
"""
Test OID Lookup Coverage

Tests the OID lookup system with various OIDs to verify coverage
and identify any issues with different lookup sources.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from reusable.oid_lookup import OIDLookup, decode_device_oid


# Test OIDs covering different categories
TEST_OIDS = {
    "Standard SNMP MIB-2": [
        "1.3.6.1.2.1.1.1.0",  # sysDescr
        "1.3.6.1.2.1.1.3.0",  # sysUpTime
        "1.3.6.1.2.1.1.5.0",  # sysName
        "1.3.6.1.2.1.2.2.1.2",  # ifDescr
        "1.3.6.1.2.1.2.2.1.3",  # ifType
    ],
    "Enterprise OIDs": [
        "1.3.6.1.4.1.12356",  # Fortinet
        "1.3.6.1.4.1.9",  # Cisco
        "1.3.6.1.4.1.2636",  # Juniper
    ],
    "Device OID Strings": [
        "1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51",  # FortiAP example
        "1.16.70.80.50.50.49.70.84.70.50.48.48.51.53.57.51",  # FortiAP example 2
    ],
    "Common Network OIDs": [
        "1.3.6.1.2.1.1.2.0",  # sysObjectID
        "1.3.6.1.2.1.1.4.0",  # sysContact
        "1.3.6.1.2.1.1.6.0",  # sysLocation
        "1.3.6.1.2.1.25.1.1.0",  # hrSystemUptime
    ],
}


def test_oid_category(category_name, oids):
    """Test a category of OIDs."""
    print(f"\n{'=' * 70}")
    print(f"Testing: {category_name}")
    print(f"{'=' * 70}")
    
    lookup = OIDLookup()
    results = {
        'found': 0,
        'not_found': 0,
        'sources': {}
    }
    
    for oid in oids:
        print(f"\nOID: {oid}")
        print("-" * 70)
        
        try:
            result = lookup.lookup(oid)
            if result:
                results['found'] += 1
                source = result.get('source', 'unknown')
                results['sources'][source] = results['sources'].get(source, 0) + 1
                
                print(f"  ✅ Found: {result.get('name', 'N/A')}")
                print(f"  Source: {source}")
                if result.get('description'):
                    desc = result.get('description', '')[:60]
                    print(f"  Description: {desc}...")
            else:
                results['not_found'] += 1
                print(f"  ❌ Not found")
                
                # Try ASCII decoding for device OIDs
                if category_name == "Device OID Strings":
                    decoded = lookup.decode_oid_ascii(oid)
                    if decoded:
                        print(f"  ⚠️  ASCII decoded: {decoded}")
        except Exception as e:
            results['not_found'] += 1
            print(f"  ❌ Error: {str(e)[:50]}")
    
    print(f"\nSummary for {category_name}:")
    print(f"  Found: {results['found']}/{len(oids)}")
    print(f"  Not Found: {results['not_found']}/{len(oids)}")
    if results['sources']:
        print(f"  Sources: {results['sources']}")
    
    return results


def test_device_oid_decoding():
    """Test device OID decoding specifically."""
    print(f"\n{'=' * 70}")
    print("Testing Device OID Decoding")
    print(f"{'=' * 70}")
    
    test_cases = [
        ("1.16.70.80.50.51.49.70.84.70.50.48.48.50.51.48.52.51", "FortiAP"),
        ("1.16.70.80.50.50.49.70.84.70.50.48.48.51.53.57.51", "FortiAP"),
        ("1.16.70.83.87.49.48.48.48.48.48.48.48.48.48.48.48", "FortiSwitch"),
    ]
    
    for oid_string, device_type in test_cases:
        print(f"\nOID: {oid_string}")
        print(f"Device Type: {device_type}")
        print("-" * 70)
        
        decoded = decode_device_oid(oid_string, device_type)
        print(f"Decoded: {decoded}")
        
        # Show ASCII breakdown
        lookup = OIDLookup()
        ascii_decoded = lookup.decode_oid_ascii(oid_string)
        if ascii_decoded:
            print(f"ASCII: {ascii_decoded}")


def test_performance():
    """Test lookup performance with caching."""
    print(f"\n{'=' * 70}")
    print("Performance Test (with caching)")
    print(f"{'=' * 70}")
    
    import time
    
    lookup = OIDLookup()
    test_oid = "1.3.6.1.2.1.1.1.0"
    
    # First lookup (cold cache)
    print(f"\nFirst lookup (cold cache):")
    start = time.time()
    result1 = lookup.lookup(test_oid)
    time1 = time.time() - start
    print(f"  Time: {time1:.3f}s")
    print(f"  Result: {result1.get('name') if result1 else 'None'}")
    
    # Second lookup (warm cache)
    print(f"\nSecond lookup (warm cache):")
    start = time.time()
    result2 = lookup.lookup(test_oid)
    time2 = time.time() - start
    print(f"  Time: {time2:.4f}s")
    print(f"  Result: {result2.get('name') if result2 else 'None'}")
    print(f"  Speedup: {time1/time2:.1f}x faster")


def main():
    """Run all tests."""
    print("=" * 70)
    print("OID Lookup Coverage Test")
    print("=" * 70)
    
    all_results = {}
    
    # Test each category
    for category, oids in TEST_OIDS.items():
        results = test_oid_category(category, oids)
        all_results[category] = results
    
    # Test device OID decoding
    test_device_oid_decoding()
    
    # Test performance
    test_performance()
    
    # Overall summary
    print(f"\n{'=' * 70}")
    print("Overall Summary")
    print(f"{'=' * 70}")
    
    total_found = sum(r['found'] for r in all_results.values())
    total_tested = sum(len(oids) for oids in TEST_OIDS.values())
    
    print(f"Total OIDs tested: {total_tested}")
    print(f"Total found: {total_found}")
    print(f"Success rate: {(total_found/total_tested)*100:.1f}%")
    
    # Source distribution
    all_sources = {}
    for results in all_results.values():
        for source, count in results['sources'].items():
            all_sources[source] = all_sources.get(source, 0) + count
    
    if all_sources:
        print(f"\nSource distribution:")
        for source, count in sorted(all_sources.items(), key=lambda x: x[1], reverse=True):
            print(f"  {source}: {count}")


if __name__ == "__main__":
    main()
