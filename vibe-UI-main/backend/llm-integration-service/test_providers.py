#!/usr/bin/env python3
"""
Test script for LLM providers
"""

import os
import sys
from llm_provider import LLMProviderFactory
from providers import OpenAIProvider, GeminiProvider, OllamaProvider

def test_provider_creation():
    """Test creating provider instances"""
    print("Testing provider creation...")
    
    # Test getting available providers
    providers = LLMProviderFactory.get_available_providers()
    print(f"Available providers: {providers}")
    
    # Test creating each provider
    for provider_name in providers:
        try:
            config = {}
            provider = LLMProviderFactory.create_provider(provider_name, config)
            print(f"✓ Successfully created {provider_name} provider")
            print(f"  Model info: {provider.get_model_info()}")
        except Exception as e:
            print(f"✗ Failed to create {provider_name} provider: {e}")

def test_openai_provider():
    """Test OpenAI provider (if API key is available)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Skipping OpenAI test (no API key found)")
        return
    
    print("Testing OpenAI provider...")
    try:
        config = {"api_key": api_key, "model": "gpt-3.5-turbo"}
        provider = LLMProviderFactory.create_provider("openai", config)
        
        # Test text generation
        result = provider.generate_text("Say hello in 3 different languages")
        print(f"✓ OpenAI text generation successful")
        print(f"  Result: {result[:100]}...")
        
        # Test model info
        info = provider.get_model_info()
        print(f"  Model info: {info}")
        
    except Exception as e:
        print(f"✗ OpenAI test failed: {e}")

def main():
    """Main test function"""
    print("LLM Provider Abstraction Test")
    print("=" * 30)
    
    test_provider_creation()
    print()
    test_openai_provider()

if __name__ == "__main__":
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()