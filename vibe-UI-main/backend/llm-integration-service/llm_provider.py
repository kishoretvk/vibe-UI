from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def __init__(self, config: Dict[str, Any]):
        """Initialize the LLM provider with configuration"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text based on the prompt"""
        pass
    
    @abstractmethod
    async def generate_text_async(self, prompt: str, **kwargs) -> str:
        """Generate text asynchronously based on the prompt"""
        pass
    
    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model being used"""
        pass

class LLMProviderFactory:
    """Factory class to create LLM provider instances"""
    
    _providers = {}
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """Register a new LLM provider"""
        cls._providers[name] = provider_class
    
    @classmethod
    def create_provider(cls, name: str, config: Dict[str, Any]) -> LLMProvider:
        """Create an instance of the specified LLM provider"""
        if name not in cls._providers:
            raise ValueError(f"Provider '{name}' is not registered")
        return cls._providers[name](config)
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available provider names"""
        return list(cls._providers.keys())