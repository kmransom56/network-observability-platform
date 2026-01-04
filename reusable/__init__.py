"""
Reusable Components Package

This package provides reusable components for API key management and AI agent frameworks
that can be easily integrated into other applications.

Modules:
    - secure_key_manager: Secure API key storage and retrieval
    - agent_framework_wrapper: Multi-backend AI agent framework
    - ai_assistant: AI-assisted audit, repair, update, optimize, and learn functions
"""

from .secure_key_manager import SecureKeyManager
from .agent_framework_wrapper import AgentFrameworkWrapper, AgentBackend
from .ai_assistant import AIAssistant
from .config import AIConfig
from .simple_ai import (
    get_ai_assistant,
    audit_file,
    repair_code,
    optimize_code,
    learn_from_codebase,
    update_dependencies,
    configure_backend
)

__all__ = [
    'SecureKeyManager',
    'AgentFrameworkWrapper',
    'AgentBackend',
    'AIAssistant',
    'AIConfig',
    'get_ai_assistant',
    'audit_file',
    'repair_code',
    'optimize_code',
    'learn_from_codebase',
    'update_dependencies',
    'configure_backend',
]

__version__ = '1.2.0'
