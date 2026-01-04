"""
FastAPI endpoints for AI Assistant

Provides REST API access to all AI backend functions.
"""

from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os

from reusable.simple_ai import (
    get_ai_assistant,
    audit_file,
    repair_code,
    optimize_code,
    learn_from_codebase,
    update_dependencies,
    configure_backend
)
from reusable.config import AIConfig
from reusable.agent_framework_wrapper import AgentBackend

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])


# Request/Response Models
class AuditRequest(BaseModel):
    target: str
    audit_type: str = "code"


class RepairRequest(BaseModel):
    issue: str
    file_path: Optional[str] = None


class OptimizeRequest(BaseModel):
    target: str
    optimization_type: str = "performance"


class LearnRequest(BaseModel):
    source: str
    topic: Optional[str] = None


class UpdateRequest(BaseModel):
    file_path: Optional[str] = None


class BackendConfigRequest(BaseModel):
    backend: str
    config: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    backend: Optional[str] = None


# Status and Configuration
@router.get("/status")
async def get_status():
    """Get AI assistant status and available backends"""
    backend = AIConfig.detect_backend()
    available = AIConfig.list_available_backends()
    
    assistant = get_ai_assistant(auto_setup=False)
    is_available = assistant and assistant.agent.is_available() if assistant else False
    
    return {
        "current_backend": backend.value if backend else None,
        "available_backends": [b.value for b in available],
        "assistant_available": is_available,
        "config_file": str(AIConfig.DEFAULT_CONFIG_FILE),
        "backends": {
            b.value: {
                "available": b in available,
                "current": b == backend
            }
            for b in AIConfig.BACKEND_PRIORITY
        }
    }


@router.get("/backends")
async def list_backends():
    """List all available backends with status"""
    available = AIConfig.list_available_backends()
    current = AIConfig.detect_backend()
    
    return {
        "backends": [
            {
                "name": b.value,
                "available": b in available,
                "current": b == current
            }
            for b in AIConfig.BACKEND_PRIORITY
        ]
    }


@router.post("/configure")
async def configure_backend_endpoint(request: BackendConfigRequest):
    """Configure AI backend"""
    try:
        backend = AgentBackend(request.backend.lower())
        AIConfig.set_backend(backend)
        
        if request.config:
            config = AIConfig.load_config()
            config["backend_config"] = request.config
            AIConfig.save_config(config)
        
        return {
            "status": "success",
            "backend": backend.value,
            "message": f"Backend configured to {backend.value}"
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid backend: {request.backend}")


# AI Operations
@router.post("/audit")
async def audit_endpoint(request: AuditRequest):
    """Audit code, configuration, or system"""
    try:
        result = audit_file(request.target, request.audit_type)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/repair")
async def repair_endpoint(request: RepairRequest):
    """Repair issues in code"""
    try:
        result = repair_code(request.issue, request.file_path)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimize")
async def optimize_endpoint(request: OptimizeRequest):
    """Optimize code"""
    try:
        result = optimize_code(request.target, request.optimization_type)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
async def learn_endpoint(request: LearnRequest):
    """Learn from codebase"""
    try:
        result = learn_from_codebase(request.source, request.topic)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update")
async def update_endpoint(request: UpdateRequest):
    """Update dependencies"""
    try:
        result = update_dependencies(request.file_path)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Chat with AI assistant"""
    try:
        backend = None
        if request.backend:
            try:
                backend = AgentBackend(request.backend.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid backend: {request.backend}")
        
        assistant = get_ai_assistant(backend=backend, auto_setup=False)
        if not assistant or not assistant.agent.is_available():
            raise HTTPException(status_code=503, detail="AI assistant not available. Configure API keys first.")
        
        response = assistant.agent.chat(request.message, request.system_prompt)
        
        return {
            "status": "success",
            "backend": assistant.agent.get_backend_name(),
            "response": response,
            "message": request.message
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    assistant = get_ai_assistant(auto_setup=False)
    return {
        "status": "healthy" if assistant and assistant.agent.is_available() else "degraded",
        "assistant_available": assistant and assistant.agent.is_available() if assistant else False
    }
