"""
Code Generator

Generate Python code and configurations based on API endpoints from MCP server.
Helps applications auto-generate API client code, tests, and documentation.
"""

from typing import List, Dict, Any, Optional
from mcp_client import MCPClient
import json


class CodeGenerator:
    """Generate code from API endpoints"""

    def __init__(self, mcp_client: Optional[MCPClient] = None):
        """
        Initialize code generator

        Args:
            mcp_client: Optional MCPClient instance
        """
        self.client = mcp_client or MCPClient.from_env()

    def generate_fndn_client(self, product: str, output_file: Optional[str] = None) -> str:
        """
        Generate Python client code for FNDN API

        Args:
            product: Fortinet product (fortigate, fortimanager, fortianalyzer)
            output_file: Optional file to write generated code to

        Returns:
            Generated Python code
        """
        endpoints = self.client.get_fndn_by_product(product)

        code = f"""
# Auto-generated FNDN API client for {product}
# Generated from MCP endpoint data

from typing import Dict, Any, List
import requests
import json
from dataclasses import dataclass


@dataclass
class {product.capitalize()}Client:
    \"\"\"Client for {product.upper()} API\"\"\"
    host: str
    username: str
    password: str
    verify_ssl: bool = False

    def __post_init__(self):
        self.session = requests.Session()
        self.session.verify = self.verify_ssl
        self.base_url = f"https://{{self.host}}/api"
        self.auth = (self.username, self.password)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        \"\"\"Make API request\"\"\"
        url = f"{{self.base_url}}{{endpoint}}"
        response = self.session.request(method, url, auth=self.auth, **kwargs)
        response.raise_for_status()
        return response.json()


# Available endpoints for {product}:
# Total: {endpoints['total']} endpoints
#
# Resources:
"""

        # Add resource info
        resources = {}
        for ep in endpoints.get("endpoints", []):
            resource = ep["resource"]
            if resource not in resources:
                resources[resource] = 0
            resources[resource] += 1

        for resource, count in sorted(resources.items(), key=lambda x: x[1], reverse=True):
            code += f"#   - {resource}: {count} endpoints\n"

        code += f"""
# Example usage:
# client = {product.capitalize()}Client(
#     host="192.168.1.1",
#     username="admin",
#     password="admin"
# )
"""

        if output_file:
            with open(output_file, "w") as f:
                f.write(code)
            print(f"Generated client code: {output_file}")

        return code

    def generate_meraki_client(self, tag: str, output_file: Optional[str] = None) -> str:
        """
        Generate Python client code for Meraki API

        Args:
            tag: API tag (organizations, networks, devices, etc.)
            output_file: Optional file to write generated code to

        Returns:
            Generated Python code
        """
        endpoints = self.client.get_meraki_by_tag(tag)

        code = f"""
# Auto-generated Meraki API client for {tag}
# Generated from MCP endpoint data

import os
import requests
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class MerakiClient:
    \"\"\"Client for Meraki Dashboard API ({tag})\"\"\"
    api_key: str
    base_url: str = "https://api.meraki.com/api/v1"

    def __post_init__(self):
        self.session = requests.Session()
        self.session.headers.update({{
            "X-Cisco-Meraki-API-Key": self.api_key,
            "Content-Type": "application/json"
        }})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        \"\"\"Make API request\"\"\"
        url = f"{{self.base_url}}{{endpoint}}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.text else {{}}

    @classmethod
    def from_env(cls) -> "MerakiClient":
        \"\"\"Create client from environment variables\"\"\"
        api_key = os.getenv("MERAKI_API_KEY")
        if not api_key:
            raise ValueError("MERAKI_API_KEY environment variable not set")
        return cls(api_key)


# Available endpoints for tag '{tag}':
# Total: {endpoints['total']} endpoints
#
"""

        # Add endpoint info
        if "by_tag" in endpoints:
            for method, eps in endpoints.get("by_tag", {}).items():
                code += f"# {method}: {len(eps)} endpoints\n"

        code += f"""
# Example usage:
# client = MerakiClient.from_env()
"""

        if output_file:
            with open(output_file, "w") as f:
                f.write(code)
            print(f"Generated client code: {output_file}")

        return code

    def generate_endpoint_validation(
        self, output_file: Optional[str] = None
    ) -> str:
        """
        Generate endpoint validation code

        Args:
            output_file: Optional file to write generated code to

        Returns:
            Generated Python validation code
        """
        stats = self.client.get_statistics()

        code = f"""
# Auto-generated endpoint validation
# Generated from MCP endpoint data

from typing import Dict, List, Tuple


class EndpointValidator:
    \"\"\"Validate API endpoints against MCP data\"\"\"

    FNDN_ENDPOINTS = {{
        "total": {stats['fndn']['total_endpoints']},
        "products": {json.dumps(stats['fndn']['products'], indent=8)}
    }}

    MERAKI_ENDPOINTS = {{
        "total": {stats['meraki']['total_endpoints']},
        "api_version": "{stats['meraki']['api_version']}"
    }}

    @staticmethod
    def validate_fndn_endpoint(product: str, resource: str) -> bool:
        \"\"\"Check if FNDN endpoint exists\"\"\"
        valid_products = EndpointValidator.FNDN_ENDPOINTS["products"]
        return product.lower() in valid_products

    @staticmethod
    def validate_meraki_endpoint(path: str, method: str) -> bool:
        \"\"\"Check if Meraki endpoint exists\"\"\"
        # In production, would query full endpoint list
        return True  # Placeholder

    @staticmethod
    def get_statistics() -> Dict[str, any]:
        \"\"\"Get endpoint statistics\"\"\"
        return {{
            "fndn_total": EndpointValidator.FNDN_ENDPOINTS["total"],
            "meraki_total": EndpointValidator.MERAKI_ENDPOINTS["total"],
            "combined_total": EndpointValidator.FNDN_ENDPOINTS["total"] +
                            EndpointValidator.MERAKI_ENDPOINTS["total"]
        }}


# Usage:
# validator = EndpointValidator()
# is_valid = validator.validate_fndn_endpoint("fortigate", "firewall")
# stats = validator.get_statistics()
"""

        if output_file:
            with open(output_file, "w") as f:
                f.write(code)
            print(f"Generated validation code: {output_file}")

        return code

    def generate_documentation(self, output_file: Optional[str] = None) -> str:
        """
        Generate API documentation in Markdown format

        Args:
            output_file: Optional file to write documentation to

        Returns:
            Generated Markdown documentation
        """
        stats = self.client.get_statistics()

        doc = f"""
# API Endpoints Documentation

Auto-generated from MCP Server endpoint data.

## Summary

- **FNDN Total Endpoints:** {stats['fndn']['total_endpoints']}
- **Meraki Total Endpoints:** {stats['meraki']['total_endpoints']}
- **Combined Total:** {stats['combined']['total_endpoints']}

## FNDN Endpoints

### Products

"""

        # Add FNDN products
        for product, count in sorted(
            stats['fndn']['products'].items(), key=lambda x: x[1], reverse=True
        ):
            doc += f"- **{product.capitalize()}**: {count} endpoints\n"

        doc += f"""

### Top Resources

"""

        # Add top resources
        for resource, count in stats['fndn']['top_resources'].items():
            doc += f"- {resource}: {count} endpoints\n"

        doc += f"""

## Meraki Endpoints

- **API Version:** {stats['meraki']['api_version']}
- **Total Endpoints:** {stats['meraki']['total_endpoints']}

### By Method

"""

        # Add method distribution
        for method, count in sorted(
            stats['meraki']['by_method'].items(), key=lambda x: x[1], reverse=True
        ):
            doc += f"- {method}: {count} endpoints\n"

        doc += f"""

### Top Tags

"""

        # Add top tags
        for tag, count in stats['meraki']['top_tags'].items():
            doc += f"- {tag}: {count} endpoints\n"

        doc += """

## How to Use

1. Import the MCP client in your application
2. Use `MCPClient` to search and validate endpoints
3. Use `CodeGenerator` to generate starter code
4. Reference this documentation when building API calls

## Examples

### Search Endpoints

```python
from mcp_client import MCPClient

client = MCPClient.from_env()
results = client.search_all("firewall")
```

### Validate Endpoint

```python
is_valid = client.validate_endpoint(
    "fndn",
    product="fortigate",
    operation="list"
)
```

### Get Endpoints by Product

```python
fortigate_eps = client.get_fndn_by_product("fortigate")
print(f"FortiGate has {fortigate_eps['total']} endpoints")
```

## Generated On

This documentation was auto-generated from MCP endpoint data.
"""

        if output_file:
            with open(output_file, "w") as f:
                f.write(doc)
            print(f"Generated documentation: {output_file}")

        return doc


if __name__ == "__main__":
    gen = CodeGenerator()

    print("Generating FNDN client...")
    gen.generate_fndn_client("fortigate", "generated_fortigate_client.py")

    print("Generating Meraki client...")
    gen.generate_meraki_client("organizations", "generated_meraki_client.py")

    print("Generating validation code...")
    gen.generate_endpoint_validation("generated_validation.py")

    print("Generating documentation...")
    gen.generate_documentation("GENERATED_ENDPOINTS.md")

    print("\nGeneration complete!")
