#!/usr/bin/env python3
"""
NeDi Topology Integration Module

Integrates Network Observability Platform with NeDi network discovery.
Provides device type identification, icon mapping, and topology visualization
updates using vendor-specific icons.

Usage:
    from nedi_topology_integration import NeDiTopologyIntegrator

    integrator = NeDiTopologyIntegrator()
    devices = integrator.get_topology_devices()
    devices_with_icons = integrator.enhance_devices_with_icons(devices)
    integrator.export_topology_json('topology.json')
"""

import json
import subprocess
import os
from typing import Dict, List, Optional
from pathlib import Path
import logging

from icon_vendor_mapper import VendorIconMapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NeDiTopologyIntegrator:
    """Integrates NeDi topology data with vendor-specific icon mapping."""

    # NeDi installation directory
    NEDI_PATH = Path("/var/nedi")
    NEDI_DB = os.getenv("NEDI_DB", "nedi")
    NEDI_USER = os.getenv("NEDI_USER", "nedi")
    NEDI_PASSWORD = os.getenv("NEDI_PASSWORD", "")  # Set in .env or environment

    def __init__(self, icon_mapper: Optional[VendorIconMapper] = None):
        """Initialize the NeDi topology integrator.

        Args:
            icon_mapper: Optional VendorIconMapper instance
        """
        self.icon_mapper = icon_mapper or VendorIconMapper()
        self.devices = []
        self.interfaces = []
        self.links = []

    def get_topology_devices(self) -> List[Dict]:
        """Retrieve all devices from NeDi database.

        Returns:
            List of device dictionaries with database fields
        """
        try:
            query = "SELECT * FROM nodes"
            results = self._execute_nedi_query(query)
            self.devices = results
            logger.info(f"Retrieved {len(results)} devices from NeDi")
            return results
        except Exception as e:
            logger.error(f"Error retrieving topology devices: {e}")
            return []

    def get_topology_interfaces(self, device_id: Optional[int] = None) -> List[Dict]:
        """Retrieve interfaces from NeDi database.

        Args:
            device_id: Optional device ID to filter interfaces

        Returns:
            List of interface dictionaries
        """
        try:
            if device_id:
                query = f"SELECT * FROM ports WHERE device_id = {device_id}"
            else:
                query = "SELECT * FROM ports"
            results = self._execute_nedi_query(query)
            self.interfaces = results
            logger.info(f"Retrieved {len(results)} interfaces from NeDi")
            return results
        except Exception as e:
            logger.error(f"Error retrieving topology interfaces: {e}")
            return []

    def get_topology_links(self) -> List[Dict]:
        """Retrieve network links from NeDi database.

        Returns:
            List of link dictionaries
        """
        try:
            query = "SELECT * FROM links"
            results = self._execute_nedi_query(query)
            self.links = results
            logger.info(f"Retrieved {len(results)} links from NeDi")
            return results
        except Exception as e:
            logger.error(f"Error retrieving topology links: {e}")
            return []

    def enhance_device(self, device: Dict) -> Dict:
        """Enhance a device dictionary with icon information.

        Args:
            device: Device dictionary from NeDi

        Returns:
            Enhanced device dictionary with icon data
        """
        sysname = device.get("sysname", "")
        model = device.get("model", "")

        icon_info = self.icon_mapper.get_device_icon(sysname=sysname, model=model)

        enhanced = device.copy()
        enhanced.update({
            "device_type": icon_info["device_type"],
            "vendor": icon_info["vendor"],
            "category": icon_info["category"],
            "icon_path": icon_info["icon_path"],
            "icon_file": icon_info["icon_file"],
            "icon_color": icon_info["color"],
            "device_class": icon_info["type"],
        })

        return enhanced

    def enhance_devices_with_icons(self, devices: Optional[List[Dict]] = None) -> List[Dict]:
        """Enhance all devices with vendor-specific icon information.

        Args:
            devices: List of device dictionaries (or uses self.devices if None)

        Returns:
            List of enhanced device dictionaries
        """
        if devices is None:
            devices = self.devices

        enhanced_devices = []
        for device in devices:
            enhanced_devices.append(self.enhance_device(device))

        return enhanced_devices

    def export_topology_json(self, output_path: str, include_interfaces: bool = True,
                           include_links: bool = True) -> str:
        """Export topology data as JSON with icon mapping.

        Args:
            output_path: Path to save JSON file
            include_interfaces: Include interface data
            include_links: Include link data

        Returns:
            JSON string
        """
        data = {
            "generated": str(Path(__file__).stat().st_mtime),
            "devices": self.enhance_devices_with_icons(),
            "icon_mapping": self.icon_mapper.get_all_device_types(),
        }

        if include_interfaces and self.interfaces:
            data["interfaces"] = self.interfaces

        if include_links and self.links:
            data["links"] = self.links

        json_str = json.dumps(data, indent=2, default=str)
        Path(output_path).write_text(json_str)
        logger.info(f"Exported topology to {output_path}")
        return json_str

    def export_topology_for_d3(self, output_path: str) -> str:
        """Export topology in D3.js format for visualization.

        Args:
            output_path: Path to save D3 JSON file

        Returns:
            JSON string in D3 format
        """
        devices = self.enhance_devices_with_icons()

        nodes = []
        for device in devices:
            node = {
                "id": device.get("id") or device.get("sysname"),
                "label": device.get("sysname", "Unknown"),
                "vendor": device.get("vendor"),
                "device_type": device.get("device_type"),
                "icon": device.get("icon_file"),
                "color": device.get("icon_color"),
                "ip": device.get("ip"),
                "model": device.get("model"),
                "category": device.get("category"),
                "device_class": device.get("device_class"),
            }
            nodes.append(node)

        # Create links from connections
        links = []
        for link in self.links:
            source = link.get("source_device")
            target = link.get("target_device")
            if source and target:
                links.append({
                    "source": source,
                    "target": target,
                    "bandwidth": link.get("bandwidth", "unknown"),
                    "status": link.get("status", "unknown"),
                })

        d3_data = {
            "nodes": nodes,
            "links": links,
        }

        json_str = json.dumps(d3_data, indent=2, default=str)
        Path(output_path).write_text(json_str)
        logger.info(f"Exported D3 topology to {output_path}")
        return json_str

    def generate_device_summary(self) -> Dict:
        """Generate summary statistics of discovered topology.

        Returns:
            Dictionary with topology statistics
        """
        devices = self.devices or self.get_topology_devices()

        if not devices:
            return {
                "total_devices": 0,
                "by_vendor": {},
                "by_category": {},
                "by_device_type": {},
            }

        summary = {
            "total_devices": len(devices),
            "by_vendor": {},
            "by_category": {},
            "by_device_type": {},
            "by_device_class": {},
        }

        for device in devices:
            enhanced = self.enhance_device(device)

            vendor = enhanced.get("vendor", "Unknown")
            summary["by_vendor"][vendor] = summary["by_vendor"].get(vendor, 0) + 1

            category = enhanced.get("category", "Unknown")
            summary["by_category"][category] = summary["by_category"].get(category, 0) + 1

            device_type = enhanced.get("device_type", "unknown")
            summary["by_device_type"][device_type] = summary["by_device_type"].get(device_type, 0) + 1

            device_class = enhanced.get("device_class", "unknown")
            summary["by_device_class"][device_class] = summary["by_device_class"].get(device_class, 0) + 1

        return summary

    def print_topology_report(self) -> None:
        """Print a formatted report of the network topology."""
        devices = self.enhance_devices_with_icons()
        summary = self.generate_device_summary()

        print("\n" + "=" * 80)
        print("NETWORK TOPOLOGY REPORT")
        print("=" * 80)

        print(f"\nTotal Devices: {summary['total_devices']}")

        if summary["by_vendor"]:
            print("\nDevices by Vendor:")
            for vendor, count in sorted(summary["by_vendor"].items()):
                print(f"  {vendor}: {count}")

        if summary["by_category"]:
            print("\nDevices by Category:")
            for category, count in sorted(summary["by_category"].items()):
                print(f"  {category}: {count}")

        print("\nDevice Details:")
        print("-" * 80)
        for device in sorted(devices, key=lambda x: x.get("sysname", "")):
            sysname = device.get("sysname", "Unknown")
            ip = device.get("ip", "N/A")
            vendor = device.get("vendor", "Unknown")
            category = device.get("category", "Unknown")
            icon_file = device.get("icon_file", "unknown.svg")

            print(f"\n{sysname}")
            print(f"  IP: {ip}")
            print(f"  Vendor: {vendor}")
            print(f"  Category: {category}")
            print(f"  Icon: {icon_file}")
            print(f"  Color: {device.get('icon_color')}")

    def _execute_nedi_query(self, query: str) -> List[Dict]:
        """Execute a query against NeDi database.

        Args:
            query: MySQL query string

        Returns:
            List of result dictionaries
        """
        try:
            # Use mysql client to execute query
            cmd = [
                "mysql",
                f"-u{self.NEDI_USER}",
                f"-p{self.NEDI_PASSWORD}",
                self.NEDI_DB,
                "-e",
                query + " \\G",
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                logger.error(f"MySQL error: {result.stderr}")
                return []

            return self._parse_mysql_output(result.stdout)

        except subprocess.TimeoutExpired:
            logger.error("MySQL query timeout")
            return []
        except Exception as e:
            logger.error(f"Error executing NeDi query: {e}")
            return []

    def _parse_mysql_output(self, output: str) -> List[Dict]:
        """Parse mysql \\G formatted output into dictionaries.

        Args:
            output: MySQL output in \\G format

        Returns:
            List of dictionaries
        """
        results = []
        current_record = {}

        for line in output.strip().split("\n"):
            line = line.strip()

            if not line:
                if current_record:
                    results.append(current_record)
                    current_record = {}
                continue

            if ": " in line:
                key, value = line.split(": ", 1)
                current_record[key.lower().replace(" ", "_")] = value

        if current_record:
            results.append(current_record)

        return results


def main():
    """Example usage of NeDi topology integrator."""
    # Initialize integrator
    integrator = NeDiTopologyIntegrator()

    # Load topology data
    integrator.get_topology_devices()
    integrator.get_topology_interfaces()
    integrator.get_topology_links()

    # Print report
    integrator.print_topology_report()

    # Export data
    integrator.export_topology_json("/tmp/nedi_topology.json")
    integrator.export_topology_for_d3("/tmp/nedi_topology_d3.json")

    print("\n✓ Topology data exported to /tmp/")


if __name__ == "__main__":
    main()
