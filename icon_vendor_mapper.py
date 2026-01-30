#!/usr/bin/env python3
"""
Vendor-Specific Icon Mapper for Network Topology Visualization

Maps discovered network devices to vendor-specific SVG icons based on device type,
model, and manufacturer. Supports infrastructure devices (firewalls, switches, APs)
and endpoint devices (desktops, laptops, mobile).

Usage:
    mapper = VendorIconMapper()
    icon_info = mapper.get_device_icon(sysname="FortiGate-3100D", model="FG-3100D")
    print(icon_info)  # {'icon': 'fortigate-3100D.svg', 'type': 'firewall', 'vendor': 'Fortinet', 'color': '#E5A100'}
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class VendorIconMapper:
    """Maps network devices to vendor-specific SVG icons and metadata."""

    # Icon library base path
    ICON_BASE_PATH = Path("/var/nedi/icon_library")

    # Device type configurations with icon paths, patterns, and styling
    DEVICE_TYPES = {
        # Fortinet - Infrastructure Devices
        "fortigate": {
            "type": "infrastructure",
            "category": "firewall",
            "vendor": "Fortinet",
            "icon_dir": "fortigate",
            "color": "#E5A100",  # Fortinet Orange
            "priority": 100,
            "patterns": [
                r"FG-\d+",  # FG-3100D, FG-100F
                r"FWF-\d+",  # FortiWifi models
                r"FortiGate",
                r"Forti.*Gate",
            ],
            "model_mapping": {
                "FG-3100D": "fortigate-3100D.svg",
                "FG-1000D": "fortigate-1000D.svg",
                "FG-600D": "fortigate-600D.svg",
                "FG-3950": "fortigate-3950.svg",
                "FWF-60F": "fortiwifi-60F.svg",
                "FWF-61F": "fortiwifi-61F.svg",
            },
            "default_icon": "fortigate.svg",
        },
        "fortiswitch": {
            "type": "infrastructure",
            "category": "switch",
            "vendor": "Fortinet",
            "icon_dir": "fortiswitch",
            "color": "#E5A100",  # Fortinet Orange
            "priority": 90,
            "patterns": [
                r"FSW-\d+",
                r"FS-\d+",
                r"FortiSwitch",
                r"Forti.*Switch",
            ],
            "model_mapping": {
                "FSW-48F": "fortiswitch-48F.svg",
                "FSW-248D": "fortiswitch-248D.svg",
                "FSW-1024D": "fortiswitch-1024D.svg",
                "FSW-524D": "fortiswitch-524D.svg",
            },
            "default_icon": "fortiswitch.svg",
        },
        "fortiap": {
            "type": "infrastructure",
            "category": "access_point",
            "vendor": "Fortinet",
            "icon_dir": "fortiap",
            "color": "#E5A100",  # Fortinet Orange
            "priority": 85,
            "patterns": [
                r"FAP-\d+",
                r"FortiAP",
                r"Forti.*AP",
            ],
            "model_mapping": {
                "FAP-432F": "fortiap-432F.svg",
                "FAP-222B": "fortiap-222B.svg",
                "FAP-221C": "fortiap-221C.svg",
                "FAP-231F": "fortiap-231F.svg",
            },
            "default_icon": "fortiap.svg",
        },
        "fortimanager": {
            "type": "infrastructure",
            "category": "management",
            "vendor": "Fortinet",
            "icon_dir": "fortimanager",
            "color": "#D4A017",  # Fortinet Darker Orange
            "priority": 95,
            "patterns": [
                r"FMG-\d+",
                r"FortiManager",
            ],
            "default_icon": "fortimanager.svg",
        },
        "fortianalyzer": {
            "type": "infrastructure",
            "category": "analytics",
            "vendor": "Fortinet",
            "icon_dir": "fortianalyzer",
            "color": "#D4A017",
            "priority": 95,
            "patterns": [
                r"FAZ-\d+",
                r"FortiAnalyzer",
            ],
            "default_icon": "fortianalyzer.svg",
        },
        # Meraki - Infrastructure Devices
        "meraki-firewall": {
            "type": "infrastructure",
            "category": "firewall",
            "vendor": "Meraki",
            "icon_dir": "meraki",
            "color": "#00BCD4",  # Meraki Cyan
            "priority": 100,
            "patterns": [
                r"MX\d+",
                r"Meraki.*MX",
                r"Meraki.*Firewall",
            ],
            "default_icon": "meraki-firewall.svg",
        },
        "meraki-switch": {
            "type": "infrastructure",
            "category": "switch",
            "vendor": "Meraki",
            "icon_dir": "meraki",
            "color": "#00BCD4",
            "priority": 90,
            "patterns": [
                r"MS\d+",
                r"Meraki.*MS",
                r"Meraki.*Switch",
            ],
            "default_icon": "meraki-switch.svg",
        },
        "meraki-ap": {
            "type": "infrastructure",
            "category": "access_point",
            "vendor": "Meraki",
            "icon_dir": "meraki",
            "color": "#00BCD4",
            "priority": 85,
            "patterns": [
                r"MR\d+",
                r"Meraki.*MR",
                r"Meraki.*AP",
                r"Meraki.*WiFi",
            ],
            "default_icon": "meraki-ap.svg",
        },
        # Cisco - Infrastructure Devices
        "cisco-switch": {
            "type": "infrastructure",
            "category": "switch",
            "vendor": "Cisco",
            "icon_dir": "cisco",
            "color": "#0066CC",  # Cisco Blue
            "priority": 90,
            "patterns": [
                r"Catalyst\s*\d+",
                r"WS-C\d+",
                r"Cisco.*Switch",
            ],
            "default_icon": "cisco-switch.svg",
        },
        "cisco-router": {
            "type": "infrastructure",
            "category": "router",
            "vendor": "Cisco",
            "icon_dir": "cisco",
            "color": "#0066CC",
            "priority": 95,
            "patterns": [
                r"ISR\s*\d+",
                r"ASR\s*\d+",
                r"Cisco.*Router",
            ],
            "default_icon": "cisco-router.svg",
        },
        # Endpoint Devices
        "desktop": {
            "type": "endpoint",
            "category": "desktop",
            "vendor": "Generic",
            "icon_dir": "endpoints",
            "color": "#34495E",  # Dark Gray
            "priority": 10,
            "patterns": [
                r"desktop",
                r"Desktop",
                r"PC",
                r"computer",
                r"Computer",
                r"station\s*\d+",
            ],
            "default_icon": "desktop.svg",
        },
        "laptop": {
            "type": "endpoint",
            "category": "laptop",
            "vendor": "Generic",
            "icon_dir": "endpoints",
            "color": "#2C3E50",  # Darker Gray
            "priority": 10,
            "patterns": [
                r"laptop",
                r"Laptop",
                r"notebook",
                r"Notebook",
                r"MacBook",
                r"portable",
            ],
            "default_icon": "laptop.svg",
        },
        "mobile": {
            "type": "endpoint",
            "category": "mobile",
            "vendor": "Generic",
            "icon_dir": "endpoints",
            "color": "#16A085",  # Teal
            "priority": 10,
            "patterns": [
                r"mobile",
                r"Mobile",
                r"phone",
                r"Phone",
                r"iPhone",
                r"Android",
                r"iPad",
                r"tablet",
            ],
            "default_icon": "mobile.svg",
        },
        # Generic/Unknown
        "generic-device": {
            "type": "infrastructure",
            "category": "device",
            "vendor": "Generic",
            "icon_dir": "generic",
            "color": "#7F8C8D",  # Gray
            "priority": 1,
            "patterns": [],
            "default_icon": "device.svg",
        },
    }

    def __init__(self, icon_base_path: Optional[str] = None):
        """Initialize the vendor icon mapper.

        Args:
            icon_base_path: Path to icon library (defaults to /var/nedi/icon_library)
        """
        if icon_base_path:
            self.ICON_BASE_PATH = Path(icon_base_path)
        self._icon_cache = {}

    def get_device_icon(
        self,
        sysname: str = "",
        model: str = "",
        sysobj_id: str = "",
        hostname: str = "",
    ) -> Dict:
        """Get vendor-specific icon information for a device.

        Args:
            sysname: Device system name (e.g., "FortiGate-3100D")
            model: Device model (e.g., "FG-3100D")
            sysobj_id: SNMP sysObjectID
            hostname: Device hostname

        Returns:
            Dictionary with icon information:
            {
                'device_type': 'fortigate',
                'vendor': 'Fortinet',
                'category': 'firewall',
                'icon_path': 'fortigate/fortigate-3100D.svg',
                'icon_file': 'fortigate-3100D.svg',
                'color': '#E5A100',
                'type': 'infrastructure',
                'confidence': 0.95
            }
        """
        # Combine all device identifiers for matching
        device_identifiers = [sysname, model, hostname]
        device_identifiers = [x for x in device_identifiers if x]  # Remove empty strings

        # Try to match against known device types
        best_match = None
        best_confidence = 0.0

        for device_type, config in self.DEVICE_TYPES.items():
            confidence = self._match_device_type(device_identifiers, config)
            if confidence > best_confidence:
                best_match = device_type
                best_confidence = confidence

        # Use best match or fallback to generic device
        device_type = best_match or "generic-device"
        config = self.DEVICE_TYPES[device_type]

        # Get the specific icon file
        icon_file = self._get_icon_file(model, config)
        icon_path = f"{config['icon_dir']}/{icon_file}"

        return {
            "device_type": device_type,
            "vendor": config["vendor"],
            "category": config["category"],
            "icon_path": icon_path,
            "icon_file": icon_file,
            "color": config["color"],
            "type": config["type"],
            "confidence": best_confidence,
        }

    def get_device_icon_html(
        self,
        sysname: str = "",
        model: str = "",
        size: int = 32,
        css_class: str = "",
    ) -> str:
        """Generate HTML SVG img tag with vendor-specific icon.

        Args:
            sysname: Device system name
            model: Device model
            size: Icon size in pixels
            css_class: Optional CSS class

        Returns:
            HTML img tag with embedded vendor-specific icon
        """
        icon_info = self.get_device_icon(sysname=sysname, model=model)

        icon_url = f"/nedi/icon_library/{icon_info['icon_path']}"

        html = f'<img src="{icon_url}" '
        html += f'width="{size}" height="{size}" '
        html += f'alt="{icon_info["vendor"]} {icon_info["category"]}" '
        html += f'style="filter: drop-shadow(0 0 2px {icon_info["color"]})" '

        if css_class:
            html += f'class="{css_class}" '

        html += f'title="{icon_info["device_type"]}" />'

        return html

    def get_device_icon_url(
        self,
        sysname: str = "",
        model: str = "",
        base_url: str = "/nedi/icon_library",
    ) -> str:
        """Get the full URL to the device icon.

        Args:
            sysname: Device system name
            model: Device model
            base_url: Base URL for icon library

        Returns:
            Full URL to icon file
        """
        icon_info = self.get_device_icon(sysname=sysname, model=model)
        return f"{base_url}/{icon_info['icon_path']}"

    def identify_device_type(self, identifiers: List[str]) -> Tuple[str, float]:
        """Identify device type from a list of identifiers.

        Args:
            identifiers: List of device identifiers (sysname, model, hostname, etc.)

        Returns:
            Tuple of (device_type, confidence)
        """
        best_match = None
        best_confidence = 0.0

        for device_type, config in self.DEVICE_TYPES.items():
            confidence = self._match_device_type(identifiers, config)
            if confidence > best_confidence:
                best_match = device_type
                best_confidence = confidence

        return best_match or "generic-device", best_confidence

    def _match_device_type(self, identifiers: List[str], config: Dict) -> float:
        """Calculate match confidence for a device configuration.

        Args:
            identifiers: List of device identifiers
            config: Device type configuration

        Returns:
            Confidence score from 0.0 to 1.0
        """
        if not config.get("patterns"):
            return 0.0

        max_confidence = 0.0

        for identifier in identifiers:
            if not identifier:
                continue

            for pattern in config["patterns"]:
                if re.search(pattern, identifier, re.IGNORECASE):
                    # Exact matches get higher confidence
                    if identifier.upper() in pattern.upper():
                        confidence = 0.95
                    else:
                        confidence = 0.75

                    max_confidence = max(max_confidence, confidence)

        return max_confidence

    def _get_icon_file(self, model: str, config: Dict) -> str:
        """Get the icon filename for a device model.

        Args:
            model: Device model
            config: Device type configuration

        Returns:
            Icon filename
        """
        if not model:
            return config.get("default_icon", "device.svg")

        # Check model mapping first
        model_mapping = config.get("model_mapping", {})
        if model in model_mapping:
            return model_mapping[model]

        # Try case-insensitive lookup
        for key, value in model_mapping.items():
            if key.upper() == model.upper():
                return value

        # Return default icon
        return config.get("default_icon", "device.svg")

    def get_all_device_types(self) -> Dict:
        """Get all configured device types and their metadata.

        Returns:
            Dictionary mapping device types to their configurations
        """
        return {
            device_type: {
                "vendor": config["vendor"],
                "category": config["category"],
                "type": config["type"],
                "color": config["color"],
                "priority": config["priority"],
            }
            for device_type, config in self.DEVICE_TYPES.items()
        }

    def get_vendor_devices(self, vendor: str) -> List[Dict]:
        """Get all device types for a specific vendor.

        Args:
            vendor: Vendor name (e.g., "Fortinet", "Meraki", "Cisco")

        Returns:
            List of device type configurations for the vendor
        """
        return [
            {
                "device_type": device_type,
                **config
            }
            for device_type, config in self.DEVICE_TYPES.items()
            if config.get("vendor") == vendor
        ]

    def export_icon_mapping_json(self, output_path: Optional[str] = None) -> str:
        """Export icon mapping as JSON for frontend use.

        Args:
            output_path: Path to save JSON file (optional)

        Returns:
            JSON string with icon mapping data
        """
        mapping = {
            "device_types": self.get_all_device_types(),
            "vendors": list(set(config["vendor"] for config in self.DEVICE_TYPES.values())),
            "icon_base_path": str(self.ICON_BASE_PATH),
            "total_types": len(self.DEVICE_TYPES),
        }

        json_str = json.dumps(mapping, indent=2)

        if output_path:
            Path(output_path).write_text(json_str)

        return json_str


# Convenience functions
def create_mapper(icon_base_path: Optional[str] = None) -> VendorIconMapper:
    """Create a new VendorIconMapper instance."""
    return VendorIconMapper(icon_base_path)


if __name__ == "__main__":
    # Example usage
    mapper = VendorIconMapper()

    # Test device identification
    test_devices = [
        ("FortiGate-3100D", "FG-3100D"),
        ("FortiSwitch-248D", "FSW-248D"),
        ("FortiAP-222B", "FAP-222B"),
        ("laptop", ""),
        ("desktop computer", ""),
        ("iPhone-12", ""),
    ]

    print("Device Icon Mapping Examples:")
    print("=" * 80)

    for sysname, model in test_devices:
        icon_info = mapper.get_device_icon(sysname=sysname, model=model)
        print(f"\nDevice: {sysname} (Model: {model})")
        print(f"  Type: {icon_info['device_type']}")
        print(f"  Vendor: {icon_info['vendor']}")
        print(f"  Category: {icon_info['category']}")
        print(f"  Icon: {icon_info['icon_path']}")
        print(f"  Color: {icon_info['color']}")
        print(f"  Confidence: {icon_info['confidence']:.0%}")
