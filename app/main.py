"""
Main FastAPI Application

Network Observability Platform API server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Import API routers
try:
    from app.api.ai_assistant import router as ai_router
except ImportError:
    # Fallback if app structure doesn't exist yet
    ai_router = None

app = FastAPI(
    title="Network Observability Platform",
    description="Comprehensive network observability and management platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
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
            "ai_assistant": "/api/ai/status"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
