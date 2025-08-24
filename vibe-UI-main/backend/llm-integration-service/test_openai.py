#!/usr/bin/env python3
"""
Test script for OpenAI integration
"""

import os
import sys
import json
from openai_integration import OpenAIIntegration

def test_basic_completion():
    """Test basic text completion"""
    print("Testing basic text completion...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Skipping test (no OPENAI_API_KEY environment variable found)")
            return
        
        openai_client = OpenAIIntegration()
        
        result = openai_client.generate_completion("Say hello in 3 different languages")
        print(f"✓ Basic completion successful")
        print(f"  Result: {result}")
        
    except Exception as e:
        print(f"✗ Basic completion failed: {e}")

def test_storytelling_insights():
    """Test storytelling insights generation"""
    print("\nTesting storytelling insights generation...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Skipping test (no OPENAI_API_KEY environment variable found)")
            return
        
        openai_client = OpenAIIntegration()
        
        data_description = "Monthly sales data for a retail company showing revenue trends over 12 months"
        data_sample = "January: $120,000, February: $110,000, March: $140,000, April: $130,000"
        
        result = openai_client.generate_storytelling_insights(data_description, data_sample)
        print(f"✓ Storytelling insights generation successful")
        print(f"  Result: {result[:200]}...")
        
    except Exception as e:
        print(f"✗ Storytelling insights generation failed: {e}")

def test_chart_description():
    """Test chart description generation"""
    print("\nTesting chart description generation...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Skipping test (no OPENAI_API_KEY environment variable found)")
            return
        
        openai_client = OpenAIIntegration()
        
        data_description = "Quarterly revenue data for different product categories"
        chart_type = "bar"
        
        result = openai_client.generate_chart_description(data_description, chart_type)
        print(f"✓ Chart description generation successful")
        print(f"  Result: {result[:200]}...")
        
    except Exception as e:
        print(f"✗ Chart description generation failed: {e}")

def test_embedding():
    """Test embedding generation"""
    print("\nTesting embedding generation...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Skipping test (no OPENAI_API_KEY environment variable found)")
            return
        
        openai_client = OpenAIIntegration()
        
        text = "This is a sample text for embedding generation"
        embedding = openai_client.get_embedding(text)
        print(f"✓ Embedding generation successful")
        print(f"  Embedding length: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
        
    except Exception as e:
        print(f"✗ Embedding generation failed: {e}")

def test_model_info():
    """Test model info retrieval"""
    print("\nTesting model info retrieval...")
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Skipping test (no OPENAI_API_KEY environment variable found)")
            return
        
        openai_client = OpenAIIntegration()
        info = openai_client.get_model_info()
        print(f"✓ Model info retrieval successful")
        print(f"  Model info: {info}")
        
    except Exception as e:
        print(f"✗ Model info retrieval failed: {e}")

def main():
    """Main test function"""
    print("OpenAI Integration Test")
    print("=" * 30)
    
    test_basic_completion()
    test_storytelling_insights()
    test_chart_description()
    test_embedding()
    test_model_info()

if __name__ == "__main__":
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()