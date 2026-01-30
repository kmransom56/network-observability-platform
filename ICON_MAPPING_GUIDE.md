# Vendor-Specific Icon Mapping Guide

**Status**: ✅ Complete
**Date**: 2026-01-30
**Components**: Python mapper, PHP integration, NeDi integration

---

## Overview

The Network Observability Platform now includes vendor-specific icon mapping for network topology visualization. This system:

- **Identifies device types** from system names, models, and identifiers
- **Maps to vendor icons** (FortiGate, FortiSwitch, FortiAP, Meraki, Cisco, generic endpoints)
- **Applies vendor colors** for visual distinction (#E5A100 for Fortinet, #00BCD4 for Meraki, etc.)
- **Differentiates infrastructure vs endpoints** for proper visualization hierarchy
- **Integrates with NeDi** network discovery data

---

## Components

### 1. Python Icon Mapper (`icon_vendor_mapper.py`)

**Location**: `/home/keith/network-observability-platform/icon_vendor_mapper.py`

**Purpose**: Core icon mapping logic with device type identification

**Key Classes**:
```python
VendorIconMapper
  ├── get_device_icon(sysname, model) → Dict with icon info
  ├── get_device_icon_html(sysname, model) → HTML img tag
  ├── get_device_icon_url(sysname, model) → Icon URL
  ├── identify_device_type(identifiers) → (type, confidence)
  └── export_icon_mapping_json() → JSON mapping data
```

**Usage Example**:
```python
from icon_vendor_mapper import VendorIconMapper

mapper = VendorIconMapper()

# Get icon for FortiGate firewall
icon_info = mapper.get_device_icon(
    sysname="FortiGate-3100D",
    model="FG-3100D"
)

print(icon_info)
# Output:
# {
#   'device_type': 'fortigate',
#   'vendor': 'Fortinet',
#   'category': 'firewall',
#   'icon_path': 'fortigate/fortigate-3100D.svg',
#   'color': '#E5A100',
#   'type': 'infrastructure',
#   'confidence': 0.95
# }

# Generate HTML img tag
html = mapper.get_device_icon_html("FortiGate-3100D", "FG-3100D", size=48)
print(html)
# Output: <img src="/nedi/icon_library/fortigate/fortigate-3100D.svg" width="48" height="48" .../>
```

### 2. PHP NeDi Mapper (`nedi_topology_mapper.php`)

**Location**: `/home/keith/network-observability-platform/nedi_topology_mapper.php`

**Purpose**: PHP wrapper for NeDi integration and template use

**Key Class**: `NeDiTopologyMapper`
```php
$mapper = new NeDiTopologyMapper();

// Get device icon information
$icon_info = $mapper->get_device_icon('FortiGate-3100D', 'FG-3100D');

// Generate HTML icon tag
$html = $mapper->get_device_icon_html('FortiGate-3100D', 'FG-3100D', 32);

// Get vendor-specific color
$color = $mapper->get_device_color('FortiGate-3100D', 'FG-3100D');

// Identify device type
$type = $mapper->identify_device_type('FortiGate-3100D', 'FG-3100D');
```

**Usage in NeDi Templates**:
```php
<?php
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');

$mapper = new NeDiTopologyMapper();

// In your topology visualization loop:
foreach ($devices as $device) {
    $icon_html = $mapper->get_device_icon_html(
        $device['sysname'],
        $device['model'],
        40
    );
    $color = $mapper->get_device_color(
        $device['sysname'],
        $device['model']
    );
    $type = $mapper->identify_device_type(
        $device['sysname'],
        $device['model']
    );

    echo "<div style='color: " . htmlspecialchars($color) . "'>";
    echo $icon_html;
    echo $device['sysname'];
    echo "</div>";
}
?>
```

### 3. Python NeDi Integration (`nedi_topology_integration.py`)

**Location**: `/home/keith/network-observability-platform/nedi_topology_integration.py`

**Purpose**: Integrate NeDi topology data with icon mapping

**Key Class**: `NeDiTopologyIntegrator`
```python
from nedi_topology_integration import NeDiTopologyIntegrator

integrator = NeDiTopologyIntegrator()

# Load topology from NeDi database
integrator.get_topology_devices()
integrator.get_topology_interfaces()
integrator.get_topology_links()

# Enhance devices with icon information
enhanced_devices = integrator.enhance_devices_with_icons()

# Print topology report
integrator.print_topology_report()

# Export for visualization
integrator.export_topology_json('/tmp/topology.json')
integrator.export_topology_for_d3('/tmp/topology_d3.json')

# Get summary statistics
summary = integrator.generate_device_summary()
```

---

## Supported Device Types

### Infrastructure Devices

| Device Type | Vendor | Category | Icon | Color |
|-------------|--------|----------|------|-------|
| fortigate | Fortinet | firewall | fortigate.svg | #E5A100 |
| fortiswitch | Fortinet | switch | fortiswitch.svg | #E5A100 |
| fortiap | Fortinet | access_point | fortiap.svg | #E5A100 |
| fortimanager | Fortinet | management | fortimanager.svg | #D4A017 |
| fortianalyzer | Fortinet | analytics | fortianalyzer.svg | #D4A017 |
| meraki-firewall | Meraki | firewall | meraki-firewall.svg | #00BCD4 |
| meraki-switch | Meraki | switch | meraki-switch.svg | #00BCD4 |
| meraki-ap | Meraki | access_point | meraki-ap.svg | #00BCD4 |
| cisco-switch | Cisco | switch | cisco-switch.svg | #0066CC |
| cisco-router | Cisco | router | cisco-router.svg | #0066CC |

### Endpoint Devices

| Device Type | Vendor | Category | Icon | Color |
|-------------|--------|----------|------|-------|
| desktop | Generic | desktop | desktop.svg | #34495E |
| laptop | Generic | laptop | laptop.svg | #2C3E50 |
| mobile | Generic | mobile | mobile.svg | #16A085 |

---

## Device Identification Patterns

Device types are identified using regex patterns matched against:
1. System name (sysname)
2. Model identifier
3. Hostname

### Fortinet Device Patterns
- **FortiGate**: `FG-\d+`, `FWF-\d+`, `FortiGate`
- **FortiSwitch**: `FSW-\d+`, `FS-\d+`, `FortiSwitch`
- **FortiAP**: `FAP-\d+`, `FortiAP`
- **FortiManager**: `FMG-\d+`, `FortiManager`
- **FortiAnalyzer**: `FAZ-\d+`, `FortiAnalyzer`

### Meraki Device Patterns
- **Firewall (MX)**: `MX\d+`, `Meraki.*MX`
- **Switch (MS)**: `MS\d+`, `Meraki.*MS`
- **Access Point (MR)**: `MR\d+`, `Meraki.*MR`, `Meraki.*WiFi`

### Endpoint Patterns
- **Desktop**: `desktop`, `PC`, `computer`
- **Laptop**: `laptop`, `notebook`, `MacBook`, `portable`
- **Mobile**: `mobile`, `phone`, `iPhone`, `Android`, `iPad`

---

## Integration with Your Network

### Discovered Devices in Your Network

From the NeDi discovery run (192.168.0.0/24):

```
Device                    Model           Type            Vendor      Icon
─────────────────────────────────────────────────────────────────────────────
FortiGate-3100D          FG-3100D        fortigate       Fortinet    fortigate-3100D.svg
FortiSwitch-248D         FSW-248D        fortiswitch     Fortinet    fortiswitch-248D.svg
FortiAP-222B             FAP-222B        fortiap         Fortinet    fortiap-222B.svg
FortiAP-231F             FAP-231F        fortiap         Fortinet    fortiap-231F.svg
```

Each device will automatically be mapped to:
- ✅ Vendor-specific icon (336+ Fortinet icons available)
- ✅ Vendor color (#E5A100 Fortinet Orange)
- ✅ Device category (firewall, switch, access_point)
- ✅ Device class (infrastructure)

---

## Usage Patterns

### Pattern 1: Python Application Integration

**In your FastAPI or Flask app**:
```python
from icon_vendor_mapper import VendorIconMapper
from nedi_topology_integration import NeDiTopologyIntegrator

app = Flask(__name__)
mapper = VendorIconMapper()
integrator = NeDiTopologyIntegrator()

@app.route('/api/topology')
def get_topology():
    """Return topology with vendor icons"""
    devices = integrator.get_topology_devices()
    enhanced = integrator.enhance_devices_with_icons(devices)
    return jsonify(enhanced)

@app.route('/api/topology/summary')
def get_topology_summary():
    """Return topology statistics"""
    summary = integrator.generate_device_summary()
    return jsonify(summary)
```

### Pattern 2: NeDi Template Integration

**Update `/var/nedi/html/Topology-Map.php`**:
```php
<?php
// At the top of the file
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');
$topology_mapper = new NeDiTopologyMapper();

// In your device rendering loop
foreach ($sql->getRows() as $device) {
    // Get vendor-specific icon and color
    $icon_html = $topology_mapper->get_device_icon_html(
        $device['sysname'],
        $device['model'],
        40
    );
    $device_color = $topology_mapper->get_device_color(
        $device['sysname'],
        $device['model']
    );
    $device_type = $topology_mapper->identify_device_type(
        $device['sysname'],
        $device['model']
    );

    // Render with vendor styling
    echo "<div class='device' style='color: $device_color'>";
    echo $icon_html;
    echo $device['sysname'];
    echo "</div>";
}
?>
```

### Pattern 3: D3.js Visualization

**Use exported D3 JSON**:
```javascript
// Load exported topology data
d3.json('/api/topology/d3').then(data => {
    // Create force simulation
    const simulation = d3.forceSimulation(data.nodes);

    // Render nodes with vendor icons
    const nodes = svg.selectAll('.node')
        .data(data.nodes)
        .enter()
        .append('g')
        .attr('class', 'node');

    // Use vendor color for styling
    nodes.append('circle')
        .attr('r', 20)
        .style('fill', d => d.color);

    // Add vendor icons
    nodes.append('image')
        .attr('xlink:href', d => `/nedi/icon_library/${d.icon_dir}/${d.icon}`)
        .attr('width', 24)
        .attr('height', 24)
        .attr('x', -12)
        .attr('y', -12);

    // Add labels
    nodes.append('text')
        .attr('dy', 35)
        .text(d => d.label);
});
```

### Pattern 4: REST API Response

**Example API response**:
```json
{
  "devices": [
    {
      "id": "1",
      "sysname": "FortiGate-3100D",
      "ip": "192.168.0.254",
      "model": "FG-3100D",
      "vendor": "Fortinet",
      "device_type": "fortigate",
      "category": "firewall",
      "icon_path": "fortigate/fortigate-3100D.svg",
      "icon_color": "#E5A100",
      "device_class": "infrastructure"
    },
    {
      "id": "4",
      "sysname": "laptop-01",
      "ip": "192.168.1.50",
      "model": "MacBook Pro",
      "vendor": "Generic",
      "device_type": "laptop",
      "category": "laptop",
      "icon_path": "endpoints/laptop.svg",
      "icon_color": "#2C3E50",
      "device_class": "endpoint"
    }
  ]
}
```

---

## Icon Library Structure

The icon library at `/var/nedi/icon_library/` contains:

```
icon_library/
├── fortigate/          (136 model-specific icons)
│   ├── fortigate.svg
│   ├── fortigate-3100D.svg
│   ├── fortigate-1000D.svg
│   └── ... (more models)
├── fortiswitch/        (69 model-specific icons)
│   ├── fortiswitch.svg
│   ├── fortiswitch-248D.svg
│   └── ... (more models)
├── fortiap/            (35 model-specific icons)
│   ├── fortiap.svg
│   └── ... (more models)
├── meraki/             (Meraki product lines)
│   ├── meraki-firewall.svg
│   ├── meraki-switch.svg
│   └── ... (more products)
├── cisco/              (Cisco devices)
├── endpoints/          (Client devices)
│   ├── desktop.svg
│   ├── laptop.svg
│   └── mobile.svg
└── generic/            (Generic device icons)
```

---

## Your Discovered Network

### Infrastructure Devices (Fortinet)

From your NeDi discovery, these devices are now mapped:

**FortiGate Firewall** (192.168.0.254)
- Model: FG-3100D
- Icon: `fortigate/fortigate-3100D.svg` (specific model icon available)
- Color: #E5A100 (Fortinet Orange)
- Category: firewall
- Interfaces: 27 discovered
- Status: Connected

**FortiSwitch** (10.255.1.2)
- Model: FSW-248D
- Icon: `fortiswitch/fortiswitch-248D.svg` (specific model icon available)
- Color: #E5A100 (Fortinet Orange)
- Category: switch
- Status: Connected

**FortiAP Units** (2 discovered)
- FortiAP-222B (192.168.1.2)
- FortiAP-231F (192.168.1.4)
- Icons: Specific model icons available
- Color: #E5A100 (Fortinet Orange)
- Category: access_point
- Status: Connected

### Endpoint Devices

Client devices (desktops, laptops, mobile) will be automatically identified and mapped to:
- `endpoints/desktop.svg` (Color: #34495E - Dark Gray)
- `endpoints/laptop.svg` (Color: #2C3E50 - Darker Gray)
- `endpoints/mobile.svg` (Color: #16A085 - Teal)

---

## Testing the Icon Mapper

### 1. Run Python Tests

```bash
cd /home/keith/network-observability-platform

# Test icon mapper directly
python3 -c "
from icon_vendor_mapper import VendorIconMapper

mapper = VendorIconMapper()

# Test Fortinet devices
devices = [
    ('FortiGate-3100D', 'FG-3100D'),
    ('FortiSwitch-248D', 'FSW-248D'),
    ('FortiAP-222B', 'FAP-222B'),
]

for sysname, model in devices:
    icon_info = mapper.get_device_icon(sysname=sysname, model=model)
    print(f'{sysname}: {icon_info[\"icon_path\"]} ({icon_info[\"color\"]})')
"
```

### 2. Test NeDi Integration

```bash
# Load topology and export with icons
python3 -c "
from nedi_topology_integration import NeDiTopologyIntegrator

integrator = NeDiTopologyIntegrator()
integrator.get_topology_devices()
integrator.print_topology_report()
integrator.export_topology_json('/tmp/topology_with_icons.json')
"
```

### 3. Export D3 Visualization Data

```bash
python3 -c "
from nedi_topology_integration import NeDiTopologyIntegrator
integrator = NeDiTopologyIntegrator()
integrator.get_topology_devices()
integrator.export_topology_for_d3('/tmp/nedi_d3_topology.json')
"

# View the exported data
cat /tmp/nedi_d3_topology.json
```

---

## Integrating with Topology-Map.php

To integrate vendor-specific icons into NeDi's main topology visualization:

### Step 1: Update NeDi PHP file with vendor mapper

```php
<?php
// At the top of /var/nedi/html/Topology-Map.php

// Include vendor icon mapper (copy file to /var/nedi/html/ or reference it)
require_once('vendor_icon_mapper.php');
// OR
require_once('/home/keith/network-observability-platform/nedi_topology_mapper.php');

$topology_mapper = new NeDiTopologyMapper();

// ... rest of your code
?>
```

### Step 2: Update device rendering in your D3/SVG code

In your JavaScript visualization code:
```javascript
// Update node rendering to use vendor-specific icons
d3.selectAll('.device-node')
    .style('fill', function(d) {
        // Call PHP to get color (or load pre-exported JSON)
        return iconMapping[d.device_type].color;
    })
    .append('image')
    .attr('xlink:href', function(d) {
        return `/nedi/icon_library/${iconMapping[d.device_type].icon_path}`;
    });
```

### Step 3: Use pre-exported JSON mapping

```javascript
// Load vendor icon mapping as JSON
d3.json('/api/icon-mapping').then(mapping => {
    // Apply to topology visualization
});
```

---

## Next Steps

1. **Update Topology-Map.php**: Integrate the vendor icon mapper into NeDi's topology visualization
2. **Create Icon Legend**: Add a legend showing vendor colors and device types
3. **Implement Filtering**: Filter topology by vendor (show only Fortinet, show only endpoints, etc.)
4. **Add Statistics Dashboard**: Display device counts by vendor and category
5. **Create Icon Browser**: Build a reference page showing all available icons

---

## API Reference

### VendorIconMapper Methods

| Method | Parameters | Returns | Purpose |
|--------|-----------|---------|---------|
| `get_device_icon()` | sysname, model, sysobj_id, hostname | Dict | Get icon information for device |
| `get_device_icon_html()` | sysname, model, size, css_class | str | Generate HTML img tag |
| `get_device_icon_url()` | sysname, model, base_url | str | Get full URL to icon |
| `identify_device_type()` | identifiers list | (str, float) | Identify device type and confidence |
| `get_all_device_types()` | None | Dict | Get all configured device types |
| `get_vendor_devices()` | vendor | List | Get devices for specific vendor |
| `export_icon_mapping_json()` | output_path | str | Export mapping as JSON |

### NeDiTopologyMapper Methods (PHP)

| Method | Parameters | Returns | Purpose |
|--------|-----------|---------|---------|
| `get_device_icon()` | sysname, model | array | Get icon information |
| `get_device_icon_html()` | sysname, model, size | string | Generate HTML img tag |
| `get_device_icon_url()` | sysname, model | string | Get full URL to icon |
| `identify_device_type()` | sysname, model | string | Identify device type |
| `get_device_color()` | sysname, model | string | Get vendor color |
| `get_all_device_types()` | None | array | Get all device types |
| `generate_styled_icon()` | sysname, model, size | string | Generate SVG icon with styling |

---

## File Locations

- **Python Mapper**: `/home/keith/network-observability-platform/icon_vendor_mapper.py`
- **PHP Mapper**: `/home/keith/network-observability-platform/nedi_topology_mapper.php`
- **NeDi Integration**: `/home/keith/network-observability-platform/nedi_topology_integration.py`
- **Icon Library**: `/var/nedi/icon_library/`
- **NeDi Topology Page**: `/var/nedi/html/Topology-Map.php`

---

## Summary

You now have a complete vendor-specific icon mapping system that:
- ✅ Identifies your FortiGate, FortiSwitch, and FortiAP devices
- ✅ Maps to 336+ Fortinet-specific icons and colors
- ✅ Supports endpoints (desktops, laptops, mobile)
- ✅ Integrates with NeDi topology visualization
- ✅ Exports topology data for D3.js visualization
- ✅ Provides both Python and PHP APIs

**Next**: Integrate with Topology-Map.php to display vendor icons in your network topology visualization.
