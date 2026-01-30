"""
Main FastAPI Application

Network Observability Platform API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# MCP Integration
try:
    from mcp_client import MCPClient
    mcp_client = MCPClient.from_env()
    mcp_stats = mcp_client.get_statistics()
    logger.info(f"MCP Server: {mcp_stats['meraki']['total_endpoints']} Meraki endpoints available")
    logger.info(f"MCP Server: {mcp_stats['fndn']['total_endpoints']} FNDN endpoints available")
except ImportError:
    logger.warning("MCP Client not available - install mcp_client.py for API validation")
    mcp_client = None
except Exception as e:
    logger.warning(f"MCP Server initialization: {e}")
    mcp_client = None

# Import API routers
try:
    from app.api.ai_assistant import router as ai_router
except ImportError:
    # Fallback if app structure doesn't exist yet
    ai_router = None

# Topology & Icon Integration (2026-01-30)
try:
    from nedi_topology_integration import NeDiTopologyIntegrator
    nedi_integrator = NeDiTopologyIntegrator()
    logger.info("NeDi topology integrator loaded")
except ImportError:
    logger.warning("NeDi topology integrator not available")
    nedi_integrator = None
except Exception as e:
    logger.warning(f"NeDi topology integration: {e}")
    nedi_integrator = None

app = FastAPI(
    title="Network Observability Platform",
    description="Comprehensive network observability and management platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nedi.netintegrate.net",
        "http://localhost:11047",
        "http://localhost:8000",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
if ai_router:
    app.include_router(ai_router)

# Serve static files
try:
    app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
except Exception:
    pass  # Static directory may not exist yet

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Network Observability Platform",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "api_docs": "/docs",
            "ai_assistant": "/api/ai/status",
            "mcp_status": "/mcp/status"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


@app.get("/mcp/status")
async def mcp_status():
    """MCP Server status endpoint"""
    if not mcp_client:
        return {
            "status": "unavailable",
            "message": "MCP client not configured"
        }

    try:
        stats = mcp_client.get_statistics()
        return {
            "status": "available",
            "meraki_endpoints": stats.get('meraki', {}).get('total_endpoints', 0),
            "fndn_endpoints": stats.get('fndn', {}).get('total_endpoints', 0),
            "total_endpoints": stats.get('meraki', {}).get('total_endpoints', 0) + stats.get('fndn', {}).get('total_endpoints', 0),
            "endpoints": {
                "meraki": stats.get('meraki', {}),
                "fndn": stats.get('fndn', {})
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Topology Endpoints with Vendor Icons (2026-01-30)

@app.get("/api/topology/devices")
async def get_topology_devices():
    """Get network topology devices from NeDi with vendor icons"""
    if not nedi_integrator:
        return {
            "status": "unavailable",
            "message": "NeDi topology integration not available"
        }

    try:
        devices = nedi_integrator.get_topology_devices()
        enhanced_devices = nedi_integrator.enhance_devices_with_icons(devices)

        return {
            "status": "success",
            "total_devices": len(enhanced_devices),
            "devices": enhanced_devices
        }
    except Exception as e:
        logger.error(f"Error getting topology devices: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/topology/summary")
async def get_topology_summary():
    """Get network topology summary by vendor and category"""
    if not nedi_integrator:
        return {
            "status": "unavailable",
            "message": "NeDi topology integration not available"
        }

    try:
        nedi_integrator.get_topology_devices()
        summary = nedi_integrator.generate_device_summary()

        return {
            "status": "success",
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Error getting topology summary: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/topology/d3")
async def get_topology_d3():
    """Get network topology in D3.js format with vendor icons"""
    if not nedi_integrator:
        return {
            "status": "unavailable",
            "message": "NeDi topology integration not available"
        }

    try:
        nedi_integrator.get_topology_devices()
        nedi_integrator.get_topology_links()

        # Export and return D3 format
        import json
        devices = nedi_integrator.enhance_devices_with_icons()

        nodes = []
        for device in devices:
            node = {
                "id": device.get("id") or device.get("sysname"),
                "label": device.get("sysname", "Unknown"),
                "vendor": device.get("vendor"),
                "device_type": device.get("device_type"),
                "icon": device.get("icon_file"),
                "color": device.get("icon_color"),
                "category": device.get("category"),
            }
            nodes.append(node)

        return {
            "status": "success",
            "nodes": nodes,
            "links": nedi_integrator.links if hasattr(nedi_integrator, 'links') else []
        }
    except Exception as e:
        logger.error(f"Error getting D3 topology: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/api/topology/icons")
async def get_icon_mapping():
    """Get vendor icon mapping configuration"""
    if not nedi_integrator:
        return {
            "status": "unavailable",
            "message": "Icon mapper not available"
        }

    try:
        icon_mapping = nedi_integrator.icon_mapper.get_all_device_types()

        return {
            "status": "success",
            "icon_mapping": icon_mapping,
            "total_types": len(icon_mapping)
        }
    except Exception as e:
        logger.error(f"Error getting icon mapping: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
