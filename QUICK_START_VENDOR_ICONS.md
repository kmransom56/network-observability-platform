# Quick Start: Vendor-Specific Icons in Network Topology

**Time Required**: 15 minutes to full integration
**Difficulty**: Easy
**Result**: Network topology with vendor-specific device icons

---

## What You'll Get

```
Before:  [generic device icon] FortiGate-3100D
         [generic device icon] FortiSwitch-248D
         [generic device icon] FortiAP-222B

After:   🔴 FortiGate-3100D (Fortinet Orange, firewall icon)
         🟠 FortiSwitch-248D (Fortinet Orange, switch icon)
         🟠 FortiAP-222B (Fortinet Orange, access_point icon)
```

---

## 5-Minute Setup

### 1. Verify Files Are Created ✓

All files are already created in your platform directory:

```bash
ls -la /home/keith/network-observability-platform/ | grep -E "(icon_vendor|nedi_topology|ICON_|VENDOR_)"
```

Expected output:
- ✅ `icon_vendor_mapper.py` (Core Python module)
- ✅ `nedi_topology_mapper.php` (NeDi integration)
- ✅ `nedi_topology_integration.py` (Database integration)
- ✅ `ICON_MAPPING_GUIDE.md` (Full documentation)
- ✅ `VENDOR_ICON_IMPLEMENTATION.md` (Implementation guide)

### 2. Test Python Icon Mapper (30 seconds)

```bash
cd /home/keith/network-observability-platform

python3 << 'EOF'
from icon_vendor_mapper import VendorIconMapper

mapper = VendorIconMapper()

# Test device identification
devices = [
    ("FortiGate-3100D", "FG-3100D"),
    ("FortiSwitch-248D", "FSW-248D"),
]

print("\n✅ Icon Mapper Tests:")
for sysname, model in devices:
    info = mapper.get_device_icon(sysname=sysname, model=model)
    print(f"  {sysname:20} → {info['icon_path']:40} ({info['color']})")
EOF
```

Expected output:
```
✅ Icon Mapper Tests:
  FortiGate-3100D          → fortigate/fortigate-3100D.svg           (#E5A100)
  FortiSwitch-248D         → fortiswitch/fortiswitch-248D.svg        (#E5A100)
```

### 3. Test PHP NeDi Integration (1 minute)

```bash
php << 'EOF'
<?php
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');

$mapper = new NeDiTopologyMapper();
$icon_url = $mapper->get_device_icon_url('FortiGate-3100D', 'FG-3100D');
$color = $mapper->get_device_color('FortiGate-3100D', 'FG-3100D');

echo "\n✅ PHP NeDi Mapper Tests:\n";
echo "  Icon URL: $icon_url\n";
echo "  Color: $color\n";
?>
EOF
```

---

## 15-Minute Integration

### Step 1: Add Icons to Topology-Map.php

Edit `/var/nedi/html/Topology-Map.php`:

```php
<?php
// Add this at the top of the file (after other includes)

// Vendor Icon Mapper Integration
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');
$topology_icon_mapper = new NeDiTopologyMapper();

// ... rest of your code ...
?>
```

### Step 2: Update Device Rendering

Find the section where devices are rendered (usually in a loop or JSON response). Replace:

**Before:**
```php
echo $device['sysname'];  // Just the name
```

**After:**
```php
// Get icon information
$icon_url = $topology_icon_mapper->get_device_icon_url(
    $device['sysname'],
    $device['model']
);
$device_color = $topology_icon_mapper->get_device_color(
    $device['sysname'],
    $device['model']
);

// Display with vendor icon and color
echo '<div style="color: ' . htmlspecialchars($device_color) . '">';
echo '<img src="' . htmlspecialchars($icon_url) . '" width="32" height="32" />';
echo ' ' . htmlspecialchars($device['sysname']);
echo '</div>';
```

### Step 3: Update JSON Responses

If Topology-Map.php returns JSON (for JavaScript visualization), add icon data:

**Before:**
```php
$response = array(
    'device' => $device['sysname'],
    'ip' => $device['ip'],
    'model' => $device['model']
);
echo json_encode($response);
```

**After:**
```php
$response = array(
    'device' => $device['sysname'],
    'ip' => $device['ip'],
    'model' => $device['model'],
    'icon_url' => $topology_icon_mapper->get_device_icon_url(
        $device['sysname'],
        $device['model']
    ),
    'icon_color' => $topology_icon_mapper->get_device_color(
        $device['sysname'],
        $device['model']
    ),
    'device_type' => $topology_icon_mapper->identify_device_type(
        $device['sysname'],
        $device['model']
    )
);
echo json_encode($response);
```

### Step 4: Update D3.js Visualization (if using)

Add icon rendering to your D3 code:

```javascript
// When rendering device nodes:
svg.selectAll('.device-icon')
    .data(devices)
    .enter()
    .append('image')
    .attr('xlink:href', d => d.icon_url)
    .attr('width', 32)
    .attr('height', 32)
    .style('filter', d => `drop-shadow(0 0 2px ${d.icon_color})`);

// Color code nodes by vendor
svg.selectAll('.device-circle')
    .style('fill', d => d.icon_color);
```

---

## Verification

### 1. Check NeDi Web Interface

```bash
# Open in browser:
http://localhost/Topology-Map.php
```

Look for:
- ✅ Fortinet device icons displayed
- ✅ Orange color (#E5A100) for Fortinet devices
- ✅ Different icons for firewall vs switch vs AP

### 2. Test API Endpoint

```bash
# Add REST endpoint to your FastAPI app
curl http://localhost:8000/api/topology/with-icons
```

Expected response should include:
```json
{
  "devices": [
    {
      "sysname": "FortiGate-3100D",
      "vendor": "Fortinet",
      "icon_path": "fortigate/fortigate-3100D.svg",
      "icon_color": "#E5A100",
      "device_type": "fortigate"
    }
  ]
}
```

### 3. Inspect Icon Files

```bash
# Verify icons exist
ls -la /var/nedi/icon_library/fortigate/ | grep -E "(fortigate|3100D)" | head -5

# Expected output:
# fortigate.svg
# fortigate-3100D.svg
# ... more model icons ...
```

---

## Troubleshooting

### Issue: PHP include fails
```
Warning: require_once(...): Failed to open stream
```

**Solution**: Verify file path:
```bash
ls -la /home/keith/network-observability-platform/nedi_topology_mapper.php
```

### Issue: Icons not displaying
```
HTTP 404: /nedi/icon_library/fortigate/fortigate-3100D.svg not found
```

**Solution**: Check icon library:
```bash
ls /var/nedi/icon_library/fortigate/ | head -10
```

### Issue: Device not identified
```
All devices showing generic-device icon
```

**Solution**: Debug device identification:
```bash
python3 << 'EOF'
from icon_vendor_mapper import VendorIconMapper
mapper = VendorIconMapper()
# Test with your actual device name
result = mapper.identify_device_type("Your-Device-Name", "Model")
print(f"Identified as: {result}")
EOF
```

---

## What Gets Added to Your Network

### Visual Changes
- ✅ Fortinet devices now show:
  - Orange color (#E5A100)
  - Device-specific icons (firewall, switch, AP)
  - Model-specific icons when available (FG-3100D.svg)

- ✅ Client devices (when discovered) show:
  - Desktop computers: Dark gray desktop icon
  - Laptops: Slightly darker gray laptop icon
  - Mobile devices: Teal mobile phone icon

### Data Enrichment
Each device now has:
- `device_type`: fortigate, fortiswitch, fortiap, etc.
- `vendor`: Fortinet, Meraki, Cisco, Generic
- `category`: firewall, switch, access_point, desktop, etc.
- `icon_path`: Path to vendor-specific SVG icon
- `icon_color`: Vendor color for styling
- `device_class`: infrastructure or endpoint

---

## Advanced: Export for D3 Visualization

Generate D3.js ready topology data:

```bash
cd /home/keith/network-observability-platform

python3 << 'EOF'
from nedi_topology_integration import NeDiTopologyIntegrator

integrator = NeDiTopologyIntegrator()
integrator.get_topology_devices()
integrator.export_topology_for_d3('/tmp/network_topology.json')

print("✅ Exported D3.js topology to /tmp/network_topology.json")
print("\nThen use in your visualization:")
print("  d3.json('/tmp/network_topology.json').then(data => { ... })")
EOF
```

---

## File Reference

| File | Usage |
|------|-------|
| `icon_vendor_mapper.py` | Python icon mapping logic |
| `nedi_topology_mapper.php` | PHP for NeDi templates |
| `nedi_topology_integration.py` | NeDi database + REST API |
| `ICON_MAPPING_GUIDE.md` | Full documentation |
| `VENDOR_ICON_IMPLEMENTATION.md` | Implementation details |
| `VENDOR_ICONS_STATUS.md` | Project status report |

---

## Summary

You now have a complete vendor icon system:

✅ **Identify devices** automatically (FortiGate → firewall, etc.)
✅ **Map to icons** (FG-3100D → fortigate-3100D.svg)
✅ **Apply colors** (#E5A100 for Fortinet, #00BCD4 for Meraki)
✅ **Export data** for visualization (JSON, D3.js)
✅ **Use in templates** (PHP/JavaScript)

**Next Steps**:
1. Add to Topology-Map.php (5 min)
2. Update rendering code (5 min)
3. Test in NeDi web interface (5 min)
4. Extend to your API (optional)

---

## Support

- **Quick Ref**: This file
- **Full Docs**: `ICON_MAPPING_GUIDE.md`
- **Implementation**: `VENDOR_ICON_IMPLEMENTATION.md`
- **Status**: `VENDOR_ICONS_STATUS.md`

**Ready to implement?** Start with Step 1 above!
