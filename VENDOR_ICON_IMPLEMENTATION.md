# Vendor Icon Implementation - Quick Reference

**Status**: ✅ Ready for Implementation
**Date**: 2026-01-30

---

## What You Have

Three complete components for vendor-specific network icons:

### 1. **Python Icon Mapper** (`icon_vendor_mapper.py`)
   - 19 device types configured
   - Support for Fortinet, Meraki, Cisco, and endpoint devices
   - Pattern-based device identification
   - 336+ model-specific icons available
   - HTML generation, JSON export, URL utilities

### 2. **PHP NeDi Mapper** (`nedi_topology_mapper.php`)
   - Drop-in NeDi template integration
   - Helper functions for direct use in PHP pages
   - Device type identification and styling
   - Icon color mapping by vendor

### 3. **NeDi Integration Module** (`nedi_topology_integration.py`)
   - Load topology from NeDi database
   - Enhance devices with icon metadata
   - Export for D3.js visualization
   - Generate topology reports
   - JSON export for frontend use

---

## Quick Implementation Steps

### Step 1: Add Icon Mapper to NeDi Topology Page

Edit `/var/nedi/html/Topology-Map.php`:

```php
<?php
// Add at the top of the file
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');
$icon_mapper = new NeDiTopologyMapper();

// ... rest of your code ...

// When rendering devices in your D3/SVG visualization:
foreach ($devices as $device) {
    $icon_url = $icon_mapper->get_device_icon_url(
        $device['sysname'],
        $device['model']
    );
    $device_color = $icon_mapper->get_device_color(
        $device['sysname'],
        $device['model']
    );

    // Use these in your visualization:
    // icon_url: /nedi/icon_library/fortigate/fortigate-3100D.svg
    // device_color: #E5A100 (Fortinet Orange)
}
?>
```

### Step 2: Update D3 Visualization

In your JavaScript code:

```javascript
// Load device data with icons
d3.json('/api/devices/with-icons').then(data => {
    // Nodes with vendor-specific styling
    svg.selectAll('.device-icon')
        .data(data.devices)
        .enter()
        .append('image')
        .attr('xlink:href', d => `/nedi/icon_library/${d.icon_path}`)
        .attr('width', 32)
        .attr('height', 32)
        .style('filter', d => `drop-shadow(0 0 2px ${d.icon_color})`);

    // Color-code nodes by vendor
    svg.selectAll('.device-circle')
        .style('fill', d => d.icon_color);
});
```

### Step 3: Export Topology with Icons

Use Python to pre-generate topology data:

```bash
# Export topology with vendor icons
python3 /home/keith/network-observability-platform/nedi_topology_integration.py

# This creates:
# /tmp/nedi_topology_icons.json - Complete topology with icon data
# /tmp/nedi_d3_topology.json    - D3.js ready format
```

### Step 4: Serve from Your Application

Add endpoint to your FastAPI app:

```python
from fastapi import FastAPI
from nedi_topology_integration import NeDiTopologyIntegrator

app = FastAPI()
integrator = NeDiTopologyIntegrator()

@app.get("/api/topology/with-icons")
async def get_topology_with_icons():
    """Return topology with vendor icons"""
    devices = integrator.get_topology_devices()
    enhanced = integrator.enhance_devices_with_icons(devices)
    return {
        "devices": enhanced,
        "icon_mapping": integrator.icon_mapper.get_all_device_types()
    }

@app.get("/api/topology/summary")
async def get_topology_summary():
    """Return topology statistics by vendor"""
    return integrator.generate_device_summary()
```

---

## Your Network - Example Icons

Based on your discovered devices:

### FortiGate Firewall (192.168.0.254)
- **Model**: FG-3100D
- **Icon**: `fortigate/fortigate-3100D.svg`
- **Color**: #E5A100 (Fortinet Orange)
- **Type**: Infrastructure → Firewall

### FortiSwitch (10.255.1.2)
- **Model**: FSW-248D
- **Icon**: `fortiswitch/fortiswitch-248D.svg`
- **Color**: #E5A100 (Fortinet Orange)
- **Type**: Infrastructure → Switch

### FortiAP Units (2x)
- **Model**: FAP-222B, FAP-231F
- **Icon**: `fortiap/fortiap-222B.svg`, `fortiap/fortiap-231F.svg`
- **Color**: #E5A100 (Fortinet Orange)
- **Type**: Infrastructure → Access Point

### Endpoint Devices (When discovered)
- **Laptops**: `endpoints/laptop.svg` (Color: #2C3E50)
- **Desktops**: `endpoints/desktop.svg` (Color: #34495E)
- **Mobile**: `endpoints/mobile.svg` (Color: #16A085)

---

## File Locations

| File | Location | Purpose |
|------|----------|---------|
| Icon Mapper | `/home/keith/network-observability-platform/icon_vendor_mapper.py` | Core Python logic |
| NeDi PHP Wrapper | `/home/keith/network-observability-platform/nedi_topology_mapper.php` | PHP/NeDi integration |
| NeDi Integration | `/home/keith/network-observability-platform/nedi_topology_integration.py` | Database + icon bridge |
| Icon Library | `/var/nedi/icon_library/` | 2,114 SVG/PNG icons |
| NeDi Topology | `/var/nedi/html/Topology-Map.php` | Main NeDi visualization |
| This Guide | `/home/keith/network-observability-platform/ICON_MAPPING_GUIDE.md` | Full documentation |

---

## Available Icons

### Fortinet (336+ icons total)
- **FortiGate**: 136 model-specific icons (FG-3100D, FG-1000D, etc.)
- **FortiSwitch**: 69 model-specific icons (FSW-248D, FSW-524D, etc.)
- **FortiAP**: 35 model-specific icons (FAP-222B, FAP-231F, etc.)
- **FortiManager**: Management appliance icons
- **FortiAnalyzer**: Analytics appliance icons

### Meraki (Complete MR, MS, MX lines)
- MX series (firewalls)
- MS series (switches)
- MR series (access points)

### Cisco
- Catalyst switches
- ISR routers
- ASR core routers

### Endpoints
- Desktop computers
- Laptops/notebooks
- Mobile devices/phones

### Generic
- Generic network devices
- Servers
- Printers
- Cameras

---

## Testing

### Test Icon Identification
```bash
python3 -c "
from icon_vendor_mapper import VendorIconMapper
mapper = VendorIconMapper()
print(mapper.get_device_icon('FortiGate-3100D', 'FG-3100D'))
"
```

### Test PHP Integration
```bash
# From your web server, test PHP mapper:
php -r "
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');
\$mapper = new NeDiTopologyMapper();
\$icon = \$mapper->get_device_icon_html('FortiGate-3100D', 'FG-3100D', 48);
echo \$icon;
"
```

### Test Topology Export
```bash
python3 nedi_topology_integration.py
# Generates:
# /tmp/nedi_topology.json (complete data)
# /tmp/nedi_d3_topology.json (D3.js format)
```

---

## Next Steps

1. **[ ] Integrate with Topology-Map.php**
   - Add vendor icon mapper include
   - Update device rendering to use icons
   - Test in NeDi web interface

2. **[ ] Create Icon Legend**
   - Show vendor colors
   - Display device categories
   - Link to icon library

3. **[ ] Update D3 Visualization**
   - Load topology from `/api/topology/with-icons`
   - Render vendor-specific icons
   - Apply vendor colors to nodes

4. **[ ] Add Filtering UI**
   - Filter by vendor (show only Fortinet, etc.)
   - Filter by device type (show only firewalls, etc.)
   - Show/hide endpoint devices

5. **[ ] Create Icon Browser**
   - Web page showing all available icons
   - Preview icons by vendor/model
   - Search/filter functionality

---

## Integration Success Indicators

✅ Icon mapper loads without errors
✅ Device types correctly identified (FortiGate → firewall, etc.)
✅ Vendor colors applied (#E5A100 for Fortinet, #00BCD4 for Meraki)
✅ SVG icons render in topology visualization
✅ Infrastructure vs endpoint devices visually distinguished
✅ Model-specific icons used when available (FG-3100D.svg, etc.)
✅ Generic device icon used as fallback

---

## Support

- **Full Documentation**: See `ICON_MAPPING_GUIDE.md`
- **API Reference**: See `ICON_MAPPING_GUIDE.md` API Reference section
- **Examples**: Check test cases in component files
- **Icon Library**: `/var/nedi/icon_library/` (2,114+ icons available)

---

## Summary

You now have a complete vendor-specific icon system ready for:
- **NeDi topology visualization** with Fortinet device icons
- **Endpoint device identification** (laptops, desktops, mobile)
- **Vendor color coding** for visual distinction
- **Model-specific icons** for detailed device representation
- **RESTful API integration** for web applications

**Status**: ✅ **READY FOR IMPLEMENTATION**

The components are tested and ready to integrate into your network topology visualization.
