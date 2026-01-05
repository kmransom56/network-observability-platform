# Fortinet MIB Integration with NeDi

This document describes the integration of Fortinet MIB files with NeDi's SNMP and FortiGate modules.

## MIB Files Location

### Source Files
- **Location:** `/home/keith/NeDi/docs/`
- **Files:**
  - `FORTINET-CORE-MIB.mib` (16 KB) - Core Fortinet enterprise OID tree
  - `FORTINET-FORTIGATE-MIB.mib` (507 KB) - FortiGate-specific MIB objects

### Installed Files
- **Location:** `/var/nedi/docs/`
- **Files:** Same as above (copied from source)

## MIB File Contents

### FORTINET-CORE-MIB.mib
Defines the base Fortinet enterprise OID tree:
- Enterprise OID: `1.3.6.1.4.1.12356` (fortinet)
- Product family assignments
- Textual conventions
- Base object identifiers

### FORTINET-FORTIGATE-MIB.mib
Defines FortiGate-specific MIB objects:
- **fnFortiGateMib** (`1.3.6.1.4.1.12356.101`) - Main FortiGate MIB tree
- **fgSystem** - System information, CPU, memory, sensors
- **fgIntf** - Interface extensions
- **fgFirewall** - Firewall policies and objects
- **fgVpn** - VPN information
- **fgWc** - Wireless controller (FortiAP management)
- **fgSw** - FortiSwitch management
- And many more...

## Integration Points

### 1. libsnmp.pm

**Location:** `/var/nedi/inc/libsnmp.pm`

**Function:** `WiFortigate()` (line ~5192)

**OIDs Used:**
```perl
# OIDs from FORTINET-FORTIGATE-MIB
# MIB files available at: /var/nedi/docs/FORTINET-CORE-MIB.mib and /var/nedi/docs/FORTINET-FORTIGATE-MIB.mib
my $sysInfoO      = "1.3.6.1.4.1.12356.101.4.1";      # fnFortiGateMib.fgSystem.fgSystemInfo
my $ifTableO      = "1.3.6.1.4.1.12356.101.7.2.1";   # fnFortiGateMib.fgIntf.fgIntfTable
my $vlanTableO     = "1.3.6.1.4.1.12356.101.7.2.2";   # fnFortiGateMib.fgIntf.fgVlanTable
my $dhcpTableO     = "1.3.6.1.4.1.12356.101.23.2.1";   # fnFortiGateMib.fgDhcp.fgDhcpTables.fgDhcpTable
my $apStaTableO    = "1.3.6.1.4.1.12356.101.14.5.1";   # fnFortiGateMib.fgWc.fgWcStaTable
```

**Usage:**
- System information retrieval
- Interface discovery
- VLAN enumeration
- DHCP server discovery
- FortiAP station table
- FortiSwitch device discovery

### 2. libfortigate.pm

**Location:** `/var/nedi/inc/libfortigate.pm`

**Note:** This module primarily uses REST API, but MIB files are documented for reference.

**Header Comment Added:**
```perl
# Fortinet MIB files available at:
# /var/nedi/docs/FORTINET-CORE-MIB.mib - Core Fortinet enterprise OID tree definitions
# /var/nedi/docs/FORTINET-FORTIGATE-MIB.mib - FortiGate-specific MIB objects
```

## OID Structure

### Enterprise Tree
```
1.3.6.1.4.1.12356 (fortinet)
  └── 101 (fnFortiGateMib)
      ├── 1 (fgModel)
      ├── 2 (fgTraps)
      ├── 3 (fgVirtualDomain)
      ├── 4 (fgSystem)
      │   ├── fgSystemInfo
      │   ├── fgSoftware
      │   ├── fgHwSensors
      │   ├── fgProcessors
      │   └── ...
      ├── 5 (fgFirewall)
      ├── 6 (fgMgmt)
      ├── 7 (fgIntf)
      ├── 8 (fgAntivirus)
      ├── 9 (fgIps)
      ├── 10 (fgApplications)
      ├── 11 (fgInetProto)
      ├── 12 (fgVpn)
      ├── 13 (fgHighAvailability)
      ├── 14 (fgWc) - Wireless Controller
      │   └── fgWcStaTable - FortiAP station table
      ├── 23 (fgDhcp)
      ├── 24 (fgSw) - FortiSwitch
      └── ...
```

## Current Usage

### SNMP Discovery (libsnmp.pm)

The `WiFortigate()` function uses these OIDs for:
1. **System Info:** `1.3.6.1.4.1.12356.101.4.1` - Version, CPU, memory
2. **Interfaces:** `1.3.6.1.4.1.12356.101.7.2.1` - Interface table
3. **VLANs:** `1.3.6.1.4.1.12356.101.7.2.2` - VLAN table
4. **DHCP:** `1.3.6.1.4.1.12356.101.23.2.1` - DHCP server table
5. **FortiAP Stations:** `1.3.6.1.4.1.12356.101.14.5.1` - Wireless client table
6. **FortiSwitch Devices:** `1.3.6.1.4.1.12356.101.24.1.1` - Managed switch table

### REST API Discovery (libfortigate.pm)

Uses FortiGate REST API instead of SNMP, but MIB files serve as:
- Documentation reference
- OID lookup for troubleshooting
- Future SNMP fallback option

## Benefits of Having MIB Files

1. **OID Lookup:** Can use MIB files with OID lookup tools
2. **Documentation:** Reference for OID meanings and structures
3. **Troubleshooting:** Understand what OIDs represent
4. **Future Enhancements:** Add more SNMP-based discovery
5. **Integration:** Works with OID lookup system (`reusable/oid_lookup.py`)

## OID Lookup Integration

The MIB files can be used with the OID lookup system:

```python
from reusable.oid_lookup import OIDLookup

lookup = OIDLookup()

# Look up Fortinet enterprise OID
result = lookup.lookup("1.3.6.1.4.1.12356")
# Result: Fortinet enterprise OID information

# Look up specific FortiGate OID
result = lookup.lookup("1.3.6.1.4.1.12356.101.4.1")
# Result: fgSystemInfo information
```

## MIB File Parsing (Future Enhancement)

Could add MIB file parsing to extract:
- OID to name mappings
- Object descriptions
- Data types
- Access levels

Example Perl code (not yet implemented):
```perl
# Parse MIB file to extract OID mappings
sub parse_fortinet_mib {
    my $mib_file = "/var/nedi/docs/FORTINET-FORTIGATE-MIB.mib";
    # Parse MIB and extract OID -> name mappings
    # Store in hash for quick lookup
}
```

## Verification

### Check MIB Files Exist
```bash
ls -lh /var/nedi/docs/*.mib
ls -lh /home/keith/NeDi/docs/*.mib
```

### Check Perl Module References
```bash
grep -n "FORTINET.*MIB\|docs.*mib" /var/nedi/inc/libsnmp.pm
grep -n "FORTINET.*MIB\|docs.*mib" /var/nedi/inc/libfortigate.pm
```

### Test OID Lookup
```bash
python3 -c "
from reusable.oid_lookup import OIDLookup
lookup = OIDLookup()
result = lookup.lookup('1.3.6.1.4.1.12356')
print(result)
"
```

## Summary

✅ **MIB Files Added:**
- Copied to `/var/nedi/docs/`
- Referenced in `libsnmp.pm` comments
- Documented in `libfortigate.pm` header

✅ **Integration Status:**
- OIDs already in use in `libsnmp.pm`
- MIB files available for reference
- Can be used with OID lookup system

✅ **Benefits:**
- Better OID understanding
- Documentation reference
- Future enhancement possibilities
- Integration with OID lookup tools

## References

- **MIB Files:** `/var/nedi/docs/FORTINET-*.mib`
- **Source Files:** `/home/keith/NeDi/docs/FORTINET-*.mib`
- **SNMP Module:** `/var/nedi/inc/libsnmp.pm` (line ~5198)
- **FortiGate Module:** `/var/nedi/inc/libfortigate.pm`
- **OID Lookup:** `reusable/oid_lookup.py`
