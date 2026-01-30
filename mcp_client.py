"""
MCP Client Utilities

Provides easy-to-use client for applications to access MCP server endpoints.
Allows applications to validate endpoints, search APIs, and generate code.
"""

import json
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import os


@dataclass
class Endpoint:
    """Represents an API endpoint from MCP server"""
    vendor: str  # "fndn" or "meraki"
    path: str
    method: str
    summary: str
    tags: List[str]
    operation_id: Optional[str] = None


class MCPClient:
    """Client for accessing MCP server endpoints"""

    def __init__(self, mcp_host: str = "127.0.0.1", mcp_port: int = 11503):
        """
        Initialize MCP client

        Args:
            mcp_host: MCP server host (default: 127.0.0.1)
            mcp_port: MCP server port (default: 11503)
        """
        self.mcp_host = mcp_host
        self.mcp_port = mcp_port
        self.base_url = f"http://{mcp_host}:{mcp_port}"
        self._cache = {}

    @classmethod
    def from_env(cls) -> "MCPClient":
        """
        Create client from environment variables

        Environment variables:
        - MCP_HOST: MCP server host (default: 127.0.0.1)
        - MCP_PORT: MCP server port (default: 11503)
        """
        host = os.getenv("MCP_HOST", "127.0.0.1")
        port = int(os.getenv("MCP_PORT", "11503"))
        return cls(host, port)

    def search_fndn(self, query: str) -> List[Dict[str, Any]]:
        """
        Search FNDN endpoints

        Args:
            query: Search term

        Returns:
            List of matching endpoints
        """
        cache_key = f"fndn_search_{query}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # This would call the actual MCP server
        # For now, return cached/static data
        try:
            from fndn_api_loader import FNDNEndpointLoader
            loader = FNDNEndpointLoader()
            results = loader.search(query)
            endpoints = [
                {
                    "vendor": "fndn",
                    "path": f"/{ep.resource}/{ep.operation}",
                    "method": "REST",
                    "product": ep.product,
                    "summary": ep.description,
                    "tags": [ep.resource]
                }
                for ep in results
            ]
            self._cache[cache_key] = endpoints
            return endpoints
        except Exception as e:
            print(f"Error searching FNDN: {e}")
            return []

    def search_meraki(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Meraki endpoints

        Args:
            query: Search term

        Returns:
            List of matching endpoints
        """
        cache_key = f"meraki_search_{query}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            from meraki_api_loader import MerakiAPILoader
            loader = MerakiAPILoader()
            results = loader.search(query)
            endpoints = [
                {
                    "vendor": "meraki",
                    "path": ep.path,
                    "method": ep.method.upper(),
                    "summary": ep.summary,
                    "tags": ep.tags,
                    "operation_id": ep.operation_id
                }
                for ep in results
            ]
            self._cache[cache_key] = endpoints
            return endpoints
        except Exception as e:
            print(f"Error searching Meraki: {e}")
            return []

    def search_all(self, query: str) -> List[Dict[str, Any]]:
        """
        Search both FNDN and Meraki endpoints

        Args:
            query: Search term

        Returns:
            List of matching endpoints from both vendors
        """
        fndn_results = self.search_fndn(query)
        meraki_results = self.search_meraki(query)
        return fndn_results + meraki_results

    def get_fndn_by_product(self, product: str) -> Dict[str, Any]:
        """
        Get FNDN endpoints by product

        Args:
            product: Product name (fortigate, fortimanager, fortianalyzer)

        Returns:
            Dictionary with endpoint list
        """
        cache_key = f"fndn_product_{product}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            from fndn_api_loader import FNDNEndpointLoader
            loader = FNDNEndpointLoader()
            results = loader.get_by_product(product)
            data = {
                "vendor": "fndn",
                "product": product,
                "total": len(results),
                "endpoints": [
                    {
                        "resource": ep.resource,
                        "operation": ep.operation,
                        "description": ep.description
                    }
                    for ep in results
                ]
            }
            self._cache[cache_key] = data
            return data
        except Exception as e:
            print(f"Error getting FNDN by product: {e}")
            return {}

    def get_meraki_by_tag(self, tag: str) -> Dict[str, Any]:
        """
        Get Meraki endpoints by tag

        Args:
            tag: Tag name

        Returns:
            Dictionary with endpoint list
        """
        cache_key = f"meraki_tag_{tag}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            from meraki_api_loader import MerakiAPILoader
            loader = MerakiAPILoader()
            results = loader.get_by_tag(tag)
            data = {
                "vendor": "meraki",
                "tag": tag,
                "total": len(results),
                "endpoints": [
                    {
                        "path": ep.path,
                        "method": ep.method.upper(),
                        "summary": ep.summary,
                        "operation_id": ep.operation_id
                    }
                    for ep in results
                ]
            }
            self._cache[cache_key] = data
            return data
        except Exception as e:
            print(f"Error getting Meraki by tag: {e}")
            return {}

    def validate_endpoint(self, vendor: str, **kwargs) -> bool:
        """
        Validate if an endpoint exists in the API documentation

        Args:
            vendor: "fndn" or "meraki"
            **kwargs: Endpoint-specific validation parameters

        Returns:
            True if endpoint exists, False otherwise
        """
        if vendor == "fndn":
            product = kwargs.get("product")
            operation = kwargs.get("operation")
            endpoints = self.get_fndn_by_product(product)
            for ep in endpoints.get("endpoints", []):
                if ep["operation"].lower() == operation.lower():
                    return True
            return False

        elif vendor == "meraki":
            path = kwargs.get("path")
            method = kwargs.get("method")
            results = self.search_meraki(path)
            for ep in results:
                if ep["path"] == path and ep["method"].upper() == method.upper():
                    return True
            return False

        return False

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available endpoints

        Returns:
            Dictionary with endpoint counts and distribution
        """
        try:
            from fndn_api_loader import FNDNEndpointLoader
            from meraki_api_loader import MerakiAPILoader

            fndn_loader = FNDNEndpointLoader()
            fndn_stats = fndn_loader.get_stats()

            meraki_loader = MerakiAPILoader()
            meraki_stats = meraki_loader.get_statistics()

            return {
                "fndn": {
                    "total_endpoints": fndn_stats["total"],
                    "products": fndn_stats["by_product"],
                    "top_resources": dict(fndn_stats["top_resources"][:5])
                },
                "meraki": {
                    "total_endpoints": meraki_stats["total_endpoints"],
                    "api_version": meraki_stats["api_version"],
                    "by_method": meraki_stats["by_method"],
                    "top_tags": dict(meraki_stats["top_tags"][:5])
                },
                "combined": {
                    "total_endpoints": fndn_stats["total"] + meraki_stats["total_endpoints"]
                }
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}


# Convenience functions
def search_endpoints(query: str) -> List[Dict[str, Any]]:
    """Quick search across all endpoints"""
    client = MCPClient.from_env()
    return client.search_all(query)


def get_fndn_endpoints(product: str) -> Dict[str, Any]:
    """Get FNDN endpoints by product"""
    client = MCPClient.from_env()
    return client.get_fndn_by_product(product)


def get_meraki_endpoints(tag: str) -> Dict[str, Any]:
    """Get Meraki endpoints by tag"""
    client = MCPClient.from_env()
    return client.get_meraki_by_tag(tag)


def validate_endpoint(vendor: str, **kwargs) -> bool:
    """Validate if an endpoint exists"""
    client = MCPClient.from_env()
    return client.validate_endpoint(vendor, **kwargs)


if __name__ == "__main__":
    # Example usage
    client = MCPClient.from_env()

    # Get statistics
    stats = client.get_statistics()
    print(f"Total FNDN endpoints: {stats['fndn']['total_endpoints']}")
    print(f"Total Meraki endpoints: {stats['meraki']['total_endpoints']}")
    print(f"Combined total: {stats['combined']['total_endpoints']}")

    # Search
    results = client.search_fndn("firewall")
    print(f"\nSearch 'firewall' in FNDN: {len(results)} results")

    # Get by product
    fortigate = client.get_fndn_by_product("fortigate")
    print(f"\nFortiGate endpoints: {fortigate['total']}")

    # Get by tag
    organizations = client.get_meraki_by_tag("organizations")
    print(f"Meraki organization endpoints: {organizations['total']}")

    # Validate
    is_valid = client.validate_endpoint("fndn", product="fortigate", operation="list")
    print(f"\nEndpoint validation: {is_valid}")
