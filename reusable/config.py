"""
Configuration Management for AI Assistant

Provides easy configuration loading and backend selection.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from .agent_framework_wrapper import AgentBackend


class AIConfig:
    """Configuration manager for AI Assistant"""
    
    DEFAULT_CONFIG_FILE = Path.home() / ".network_observability_ai_config.json"
    
    # Default backend priority order
    BACKEND_PRIORITY = [
        AgentBackend.OPENAI,
        AgentBackend.ANTHROPIC,
        AgentBackend.AUTOGEN,
        AgentBackend.MAGENTIC_ONE,
        AgentBackend.DOCKER_CAGENT,
    ]
    
    @staticmethod
    def load_config(config_file: Optional[Path] = None) -> Dict[str, Any]:
        """Load configuration from file"""
        if config_file is None:
            config_file = AIConfig.DEFAULT_CONFIG_FILE
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_file: Optional[Path] = None):
        """Save configuration to file"""
        if config_file is None:
            config_file = AIConfig.DEFAULT_CONFIG_FILE
        
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Failed to save config: {e}")
    
    @staticmethod
    def detect_backend() -> Optional[AgentBackend]:
        """Auto-detect available backend from environment variables"""
        # Check for API keys in environment
        if os.getenv("OPENAI_API_KEY"):
            return AgentBackend.OPENAI
        elif os.getenv("ANTHROPIC_API_KEY"):
            return AgentBackend.ANTHROPIC
        elif os.getenv("AUTOGEN_API_KEY"):
            return AgentBackend.AUTOGEN
        elif os.getenv("MAGENTIC_ONE_API_KEY"):
            return AgentBackend.MAGENTIC_ONE
        
        # Check config file
        config = AIConfig.load_config()
        if config.get("backend"):
            try:
                return AgentBackend(config["backend"])
            except ValueError:
                pass
        
        # Default to OpenAI if nothing found
        return AgentBackend.OPENAI
    
    @staticmethod
    def get_backend_config() -> Dict[str, Any]:
        """Get backend-specific configuration"""
        config = AIConfig.load_config()
        return config.get("backend_config", {})
    
    @staticmethod
    def set_backend(backend: AgentBackend, config_file: Optional[Path] = None):
        """Set preferred backend in configuration"""
        config = AIConfig.load_config(config_file)
        config["backend"] = backend.value
        AIConfig.save_config(config, config_file)
    
    @staticmethod
    def list_available_backends() -> list:
        """List backends with available API keys"""
        available = []
        for backend in AIConfig.BACKEND_PRIORITY:
            env_var = {
                AgentBackend.OPENAI: "OPENAI_API_KEY",
                AgentBackend.ANTHROPIC: "ANTHROPIC_API_KEY",
                AgentBackend.AUTOGEN: "AUTOGEN_API_KEY",
                AgentBackend.MAGENTIC_ONE: "MAGENTIC_ONE_API_KEY",
                AgentBackend.DOCKER_CAGENT: "DOCKER_CAGENT_API_KEY",
            }.get(backend)
            
            if env_var and os.getenv(env_var):
                available.append(backend)
        
        return available
