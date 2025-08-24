import openai
import os
from typing import Dict, Any, List, Optional

class OpenAIIntegration:
    """OpenAI integration class for handling API calls and responses"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI integration
        
        Args:
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY environment variable)
            model: Model to use for completions
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_completion(self, prompt: str, **kwargs) -> str:
        """
        Generate a completion using OpenAI API
        
        Args:
            prompt: The prompt to send to the model
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The generated completion text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_storytelling_insights(self, data_description: str, data_sample: str = "") -> Dict[str, Any]:
        """
        Generate storytelling insights from data description
        
        Args:
            data_description: Description of the data
            data_sample: Sample of the actual data (optional)
            
        Returns:
            Dictionary containing insights, trends, and recommendations
        """
        prompt = f"""
        You are an AI data analyst. Based on the following data description, provide insights in a structured format:
        
        Data Description: {data_description}
        
        Sample Data: {data_sample if data_sample else 'No sample provided'}
        
        Please provide:
        1. A brief summary of what this data represents
        2. 2-3 key insights or trends
        3. 1-2 anomalies or outliers (if any)
        4. 2-3 actionable recommendations
        
        Format your response as JSON with the following structure:
        {{
            "summary": "Brief summary",
            "insights": [
                {{"type": "trend/anomaly/insight", "description": "Description", "confidence": 0.0}}
            ],
            "recommendations": [
                "Recommendation 1",
                "Recommendation 2"
            ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst that provides structured insights in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_chart_description(self, data_description: str, chart_type: str) -> str:
        """
        Generate a description for how to visualize data in a specific chart type
        
        Args:
            data_description: Description of the data
            chart_type: Type of chart to visualize the data in
            
        Returns:
            Description of how to visualize the data
        """
        prompt = f"""
        You are a data visualization expert. Based on the following data description, 
        explain how to best visualize this data using a {chart_type} chart.
        
        Data Description: {data_description}
        
        Please provide:
        1. What data elements should be mapped to which axes or chart elements
        2. What insights this visualization would reveal
        3. Any special considerations for this chart type with this data
        
        Keep your response concise and focused.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"OpenAI Embedding API error: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": "OpenAI",
            "model": self.model,
            "api_version": "v1"
        }