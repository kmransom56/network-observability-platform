"""
Network Observability Platform API Validator

Validates FortiGate, Meraki, and SNMP API endpoints against MCP documentation.
Used by the Network Observability Platform for device management validation.
"""

import sys
from typing import Dict, Tuple, Optional, List
import logging

# Add fndn module to path
sys.path.insert(0, '/media/keith/DATASTORE4/cisco-meraki-cli/modules/fndn')

try:
    from mcp_client import MCPClient
except ImportError:
    print("Warning: MCP client not available")
    MCPClient = None

logger = logging.getLogger(__name__)


class FortiGateAPIValidator:
    """Validates FortiGate API endpoints against FNDN documentation"""

    def __init__(self, verbose: bool = False):
        """
        Initialize FortiGate validator

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.client = None

        try:
            if MCPClient:
                self.client = MCPClient.from_env()
                stats = self.client.get_statistics()
                fndn_endpoints = stats.get('fndn', {}).get('by_product', {}).get('fortigate', 0)
                logger.info(f"MCP connected: {fndn_endpoints} FortiGate endpoints")
        except Exception as e:
            logger.warning(f"MCP not available: {e}")

    def validate_endpoint(self, operation: str, resource: str = None) -> Tuple[bool, Optional[str]]:
        """
        Validate that a FortiGate endpoint exists

        Args:
            operation: API operation (e.g., 'read', 'create', 'update', 'delete')
            resource: Resource type (e.g., 'firewall', 'system', 'network')

        Returns:
            Tuple of (is_valid, description) where is_valid is True if endpoint exists
        """
        if not self.client:
            return None, "MCP client not available"

        try:
            endpoints = self.client.get_fndn_by_product('fortigate')

            for ep in endpoints.get('endpoints', []):
                if ep['operation'].lower() == operation.lower():
                    if resource is None or ep.get('resource', '').lower() == resource.lower():
                        if self.verbose:
                            logger.info(f"✓ FortiGate endpoint valid: {operation}")
                        return True, ep.get('description', '')

            if self.verbose:
                logger.warning(f"✗ FortiGate endpoint not found: {operation}")
            return False, None

        except Exception as e:
            logger.error(f"Validation error: {e}")
            return None, str(e)

    def get_endpoint_info(self, query: str) -> Dict:
        """
        Get information about FortiGate endpoints matching a query

        Args:
            query: Search query (e.g., 'firewall', 'system', 'network')

        Returns:
            Dictionary with matching endpoints
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            results = self.client.search_fndn(query)
            # Filter to FortiGate only
            fortigate_results = [ep for ep in results if ep.get('product', '') == 'fortigate']

            endpoints = [
                {
                    'operation': ep['operation'],
                    'resource': ep.get('resource', ''),
                    'description': ep.get('description', ''),
                    'product': 'fortigate'
                }
                for ep in fortigate_results[:10]  # Top 10 results
            ]

            return {
                'query': query,
                'total_results': len(fortigate_results),
                'displayed': len(endpoints),
                'endpoints': endpoints
            }

        except Exception as e:
            return {'error': str(e)}

    def get_endpoints_by_resource(self, resource: str) -> Dict:
        """
        Get all FortiGate endpoints for a specific resource type

        Args:
            resource: Resource type (e.g., 'firewall', 'system', 'network')

        Returns:
            Dictionary with endpoints grouped by operation
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            result = self.client.search_fndn(resource)
            fortigate_eps = [ep for ep in result if ep.get('product', '') == 'fortigate']

            # Group by operation type
            by_operation = {}
            for ep in fortigate_eps:
                op = ep.get('operation', 'unknown')
                if op not in by_operation:
                    by_operation[op] = []
                by_operation[op].append(ep)

            return {
                'resource': resource,
                'total': len(fortigate_eps),
                'by_operation': {k: len(v) for k, v in by_operation.items()},
                'endpoints': fortigate_eps[:15]  # Top 15
            }

        except Exception as e:
            return {'error': str(e)}

    def get_statistics(self) -> Dict:
        """
        Get FortiGate API statistics

        Returns:
            Dictionary with endpoint counts and distribution
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            stats = self.client.get_statistics()
            fndn_stats = stats.get('fndn', {})
            fortigate_count = fndn_stats.get('by_product', {}).get('fortigate', 0)

            return {
                'product': 'fortigate',
                'total_endpoints': fortigate_count,
                'by_product': fndn_stats.get('by_product', {}),
                'all_fndn': fndn_stats.get('total_endpoints', 0)
            }
        except Exception as e:
            return {'error': str(e)}

    def validate_multiple_endpoints(self, operations: List[str]) -> Dict:
        """
        Validate multiple FortiGate operations at once

        Args:
            operations: List of operation names

        Returns:
            Dictionary with validation results
        """
        results = {
            'total': len(operations),
            'valid': 0,
            'invalid': 0,
            'unknown': 0,
            'details': []
        }

        for operation in operations:
            is_valid, description = self.validate_endpoint(operation)

            if is_valid is True:
                results['valid'] += 1
                status = 'valid'
            elif is_valid is False:
                results['invalid'] += 1
                status = 'invalid'
            else:
                results['unknown'] += 1
                status = 'unknown'

            results['details'].append({
                'operation': operation,
                'status': status,
                'description': description
            })

        return results


class MerakiAPIValidator:
    """Validates Meraki API endpoints against MCP documentation"""

    def __init__(self, verbose: bool = False):
        """
        Initialize Meraki validator

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.client = None

        try:
            if MCPClient:
                self.client = MCPClient.from_env()
                stats = self.client.get_statistics()
                logger.info(f"MCP connected: {stats['meraki']['total_endpoints']} Meraki endpoints")
        except Exception as e:
            logger.warning(f"MCP not available: {e}")

    def validate_endpoint(self, path: str, method: str = "GET") -> Tuple[bool, Optional[str]]:
        """
        Validate that a Meraki endpoint exists

        Args:
            path: API endpoint path (e.g., '/organizations/{organizationId}/networks')
            method: HTTP method (GET, POST, PUT, DELETE)

        Returns:
            Tuple of (is_valid, summary) where is_valid is True if endpoint exists
        """
        if not self.client:
            return None, "MCP client not available"

        try:
            base_path = path.split('{')[0].rstrip('/')
            results = self.client.search_meraki(base_path)

            for ep in results:
                if self._path_matches(ep['path'], path) and ep['method'].upper() == method.upper():
                    if self.verbose:
                        logger.info(f"✓ Endpoint valid: {method} {path}")
                    return True, ep.get('summary', '')

            if self.verbose:
                logger.warning(f"✗ Endpoint not found: {method} {path}")
            return False, None

        except Exception as e:
            logger.error(f"Validation error: {e}")
            return None, str(e)

    def _path_matches(self, doc_path: str, request_path: str) -> bool:
        """
        Check if documented path matches request path
        Handles parameter placeholders like {organizationId}
        """
        doc_base = doc_path.split('{')[0].rstrip('/')
        req_base = request_path.split('{')[0].rstrip('/')
        return doc_base == req_base

    def get_endpoint_info(self, query: str) -> Dict:
        """
        Get information about endpoints matching a query

        Args:
            query: Search query (e.g., 'organization', 'device', 'network')

        Returns:
            Dictionary with matching endpoints
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            results = self.client.search_meraki(query)

            endpoints = [
                {
                    'method': ep['method'],
                    'path': ep['path'],
                    'summary': ep['summary'],
                    'tags': ep.get('tags', [])
                }
                for ep in results[:10]  # Top 10 results
            ]

            return {
                'query': query,
                'total_results': len(results),
                'displayed': len(endpoints),
                'endpoints': endpoints
            }

        except Exception as e:
            return {'error': str(e)}

    def get_endpoints_by_tag(self, tag: str) -> Dict:
        """
        Get all endpoints for a specific tag

        Args:
            tag: API tag (e.g., 'organizations', 'networks', 'devices')

        Returns:
            Dictionary with endpoints grouped by method
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            result = self.client.get_meraki_by_tag(tag)

            return {
                'tag': tag,
                'total': result.get('total', 0),
                'by_method': result.get('by_method', {}),
                'endpoints': result.get('endpoints', [])
            }

        except Exception as e:
            return {'error': str(e)}

    def get_statistics(self) -> Dict:
        """
        Get API statistics

        Returns:
            Dictionary with endpoint counts and distribution
        """
        if not self.client:
            return {'error': 'MCP client not available'}

        try:
            return self.client.get_statistics()
        except Exception as e:
            return {'error': str(e)}

    def validate_multiple_endpoints(self, endpoints: List[Tuple[str, str]]) -> Dict:
        """
        Validate multiple endpoints at once

        Args:
            endpoints: List of (path, method) tuples

        Returns:
            Dictionary with validation results
        """
        results = {
            'total': len(endpoints),
            'valid': 0,
            'invalid': 0,
            'unknown': 0,
            'details': []
        }

        for path, method in endpoints:
            is_valid, summary = self.validate_endpoint(path, method)

            if is_valid is True:
                results['valid'] += 1
                status = 'valid'
            elif is_valid is False:
                results['invalid'] += 1
                status = 'invalid'
            else:
                results['unknown'] += 1
                status = 'unknown'

            results['details'].append({
                'path': path,
                'method': method,
                'status': status,
                'summary': summary
            })

        return results


class NetworkDeviceValidator:
    """Validates network device management operations"""

    def __init__(self, verbose: bool = False):
        """
        Initialize network device validator

        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.fortigate = FortiGateAPIValidator(verbose=verbose)
        self.meraki = MerakiAPIValidator(verbose=verbose)

    def validate_device_operation(self, vendor: str, operation: str, resource: str = None) -> Tuple[bool, Optional[str]]:
        """
        Validate device management operation for a specific vendor

        Args:
            vendor: Device vendor ('fortigate', 'meraki', 'meraki-managed')
            operation: Operation to validate
            resource: Optional resource type

        Returns:
            Tuple of (is_valid, description)
        """
        if vendor.lower() in ['fortigate', 'fortinet']:
            return self.fortigate.validate_endpoint(operation, resource)
        elif vendor.lower() in ['meraki', 'meraki-managed']:
            # For Meraki, operation might be a path
            return self.meraki.validate_endpoint(operation, 'GET')
        else:
            return False, f"Unknown vendor: {vendor}"

    def get_vendor_capabilities(self, vendor: str) -> Dict:
        """
        Get available operations for a vendor

        Args:
            vendor: Device vendor

        Returns:
            Dictionary with available operations
        """
        if vendor.lower() in ['fortigate', 'fortinet']:
            return self.fortigate.get_statistics()
        elif vendor.lower() in ['meraki', 'meraki-managed']:
            return self.meraki.get_statistics()
        else:
            return {'error': f'Unknown vendor: {vendor}'}

    def compare_vendors(self, operation: str) -> Dict:
        """
        Compare same operation across vendors

        Args:
            operation: Operation to compare

        Returns:
            Dictionary with availability across vendors
        """
        results = {
            'operation': operation,
            'fortigate': {},
            'meraki': {},
            'available_in': []
        }

        fg_valid, fg_desc = self.fortigate.validate_endpoint(operation)
        if fg_valid:
            results['fortigate'] = {'available': True, 'description': fg_desc}
            results['available_in'].append('fortigate')
        else:
            results['fortigate'] = {'available': False}

        # Search Meraki for similar operation
        meraki_results = self.meraki.get_endpoint_info(operation)
        if meraki_results.get('total_results', 0) > 0:
            results['meraki'] = {'available': True, 'endpoints_found': meraki_results['total_results']}
            results['available_in'].append('meraki')
        else:
            results['meraki'] = {'available': False}

        return results


# Convenience functions for quick validation

def validate_fortigate_operation(operation: str, resource: str = None, verbose: bool = False) -> Tuple[bool, Optional[str]]:
    """Quick validation of FortiGate operation"""
    validator = FortiGateAPIValidator(verbose=verbose)
    return validator.validate_endpoint(operation, resource)


def validate_meraki_endpoint(path: str, method: str = "GET", verbose: bool = False) -> Tuple[bool, Optional[str]]:
    """Quick validation of Meraki endpoint"""
    validator = MerakiAPIValidator(verbose=verbose)
    return validator.validate_endpoint(path, method)


def search_fortigate_operations(query: str) -> Dict:
    """Quick search of FortiGate operations"""
    validator = FortiGateAPIValidator()
    return validator.get_endpoint_info(query)


def search_meraki_endpoints(query: str) -> Dict:
    """Quick search of Meraki endpoints"""
    validator = MerakiAPIValidator()
    return validator.get_endpoint_info(query)


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)

    print("Testing Network Observability API Validators...\n")

    # Test FortiGate validator
    print("=" * 60)
    print("FORTIGATE API VALIDATOR TEST")
    print("=" * 60)

    fortigate = FortiGateAPIValidator(verbose=True)

    # Test 1: Validate operation
    print("\n1. Validating FortiGate operation...")
    is_valid, desc = fortigate.validate_endpoint("firewall")
    print(f"   Valid: {is_valid}, Description: {desc}")

    # Test 2: Get endpoint info
    print("\n2. Searching FortiGate operations...")
    info = fortigate.get_endpoint_info("firewall")
    print(f"   Found {info.get('total_results', 0)} results")

    # Test 3: Get statistics
    print("\n3. Getting FortiGate statistics...")
    stats = fortigate.get_statistics()
    print(f"   Total endpoints: {stats.get('total_endpoints', 'N/A')}")

    # Test Meraki validator
    print("\n" + "=" * 60)
    print("MERAKI API VALIDATOR TEST")
    print("=" * 60)

    meraki = MerakiAPIValidator(verbose=True)

    # Test 1: Validate endpoint
    print("\n1. Validating Meraki endpoint...")
    is_valid, summary = meraki.validate_endpoint(
        "/organizations/{organizationId}/networks",
        "GET"
    )
    print(f"   Valid: {is_valid}, Summary: {summary}")

    # Test 2: Search endpoints
    print("\n2. Searching Meraki endpoints...")
    info = meraki.get_endpoint_info("organization")
    print(f"   Found {info.get('total_results', 0)} results")

    # Test 3: Get statistics
    print("\n3. Getting Meraki statistics...")
    stats = meraki.get_statistics()
    print(f"   Total endpoints: {stats.get('meraki', {}).get('total_endpoints', 'N/A')}")

    # Test Network Device Validator
    print("\n" + "=" * 60)
    print("NETWORK DEVICE VALIDATOR TEST")
    print("=" * 60)

    device_validator = NetworkDeviceValidator(verbose=True)

    # Test 1: Compare vendors
    print("\n1. Comparing vendors for 'firewall' operation...")
    comparison = device_validator.compare_vendors("firewall")
    print(f"   Available in: {comparison['available_in']}")

    # Test 2: Get vendor capabilities
    print("\n2. FortiGate capabilities...")
    fg_caps = device_validator.get_vendor_capabilities('fortigate')
    print(f"   Total endpoints: {fg_caps.get('total_endpoints', 'N/A')}")

    print("\n" + "=" * 60)
    print("Tests complete!")
    print("=" * 60)
