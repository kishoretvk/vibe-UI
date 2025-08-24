import openai
import google.generativeai as genai
import requests
import os
import json
from typing import Dict, Any, List
from .llm_provider import LLMProvider, LLMProviderFactory

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_text_async(self, prompt: str, **kwargs) -> str:
        """Generate text asynchronously using OpenAI API"""
        # For simplicity, we're using the sync version in async context
        # In a production environment, you might want to use aiohttp or similar
        return self.generate_text(prompt, **kwargs)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"OpenAI Embedding API error: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the OpenAI model"""
        return {
            "provider": "OpenAI",
            "model": self.model,
            "type": "chat_completion"
        }

class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key') or os.getenv('GEMINI_API_KEY')
        self.model_name = config.get('model', 'gemini-pro')
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Google Gemini API"""
        try:
            response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    async def generate_text_async(self, prompt: str, **kwargs) -> str:
        """Generate text asynchronously using Google Gemini API"""
        try:
            response = await self.model.generate_content_async(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Google Gemini API"""
        # Gemini doesn't have a direct embedding API in this version
        # This would need to be implemented based on the specific API
        raise NotImplementedError("Embedding generation not implemented for Gemini provider")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the Gemini model"""
        return {
            "provider": "Google Gemini",
            "model": self.model_name,
            "type": "generative_model"
        }

class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model = config.get('model', 'llama2')
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    **kwargs
                }
            )
            response.raise_for_status()
            
            # Ollama returns a stream of JSON objects, we need to parse them
            lines = response.text.strip().split('\n')
            full_response = ""
            for line in lines:
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        full_response += data['response']
            return full_response
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    async def generate_text_async(self, prompt: str, **kwargs) -> str:
        """Generate text asynchronously using Ollama API"""
        # For simplicity, we're using the sync version in async context
        # In a production environment, you might want to use aiohttp or similar
        return self.generate_text(prompt, **kwargs)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                }
            )
            response.raise_for_status()
            return response.json()['embedding']
        except Exception as e:
            raise Exception(f"Ollama Embedding API error: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the Ollama model"""
        return {
            "provider": "Ollama",
            "model": self.model,
            "base_url": self.base_url,
            "type": "local_model"
        }

# Register the providers with the factory
LLMProviderFactory.register_provider('openai', OpenAIProvider)
LLMProviderFactory.register_provider('gemini', GeminiProvider)
LLMProviderFactory.register_provider('ollama', OllamaProvider)