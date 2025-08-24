import os
from typing import Dict, Any

# Default configurations for LLM providers
DEFAULT_CONFIGS = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": "gpt-3.5-turbo"
    },
    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "model": "gemini-pro"
    },
    "ollama": {
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "model": "llama2"
    }
}

def get_provider_config(provider_name: str) -> Dict[str, Any]:
    """Get configuration for a specific provider"""
    return DEFAULT_CONFIGS.get(provider_name, {})