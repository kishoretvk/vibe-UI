#!/usr/bin/env python3
"""
Integration test for LLM integration service
"""

import requests
import json
import os

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5005"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check successful: {data}")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_providers_list():
    """Test the providers list endpoint"""
    print("\nTesting providers list endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/providers")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Providers list successful: {data}")
            return True
        else:
            print(f"✗ Providers list failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Providers list failed: {e}")
        return False

def test_openai_storytelling():
    """Test OpenAI storytelling endpoint"""
    print("\nTesting OpenAI storytelling endpoint...")
    try:
        # Skip if no API key
        if not os.getenv("OPENAI_API_KEY"):
            print("Skipping OpenAI test (no OPENAI_API_KEY environment variable found)")
            return True
            
        data = {
            "data_description": "Monthly finance data including revenue and expenses for a tech company",
            "data_sample": "January: Revenue $200,000, Expenses $120,000; February: Revenue $220,000, Expenses $130,000"
        }
        
        response = requests.post(f"{SERVICE_URL}/api/storytelling", json=data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ OpenAI storytelling successful")
            print(f"  Model info: {data.get('model_info', 'N/A')}")
            print(f"  Insights preview: {str(data.get('insights', ''))[:100]}...")
            return True
        else:
            print(f"✗ OpenAI storytelling failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ OpenAI storytelling failed: {e}")
        return False

def test_generic_text_generation():
    """Test generic text generation with OpenAI provider"""
    print("\nTesting generic text generation endpoint...")
    try:
        # Skip if no API key
        if not os.getenv("OPENAI_API_KEY"):
            print("Skipping OpenAI test (no OPENAI_API_KEY environment variable found)")
            return True
            
        data = {
            "provider": "openai",
            "prompt": "Explain what a data analyst does in 2 sentences.",
            "config": {
                "model": "gpt-3.5-turbo"
            }
        }
        
        response = requests.post(f"{SERVICE_URL}/api/generate", json=data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Generic text generation successful")
            print(f"  Model info: {data.get('model_info', 'N/A')}")
            print(f"  Result preview: {str(data.get('result', ''))[:100]}...")
            return True
        else:
            print(f"✗ Generic text generation failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Generic text generation failed: {e}")
        return False

def main():
    """Main test function"""
    print("LLM Integration Service Test")
    print("=" * 30)
    
    # Run tests
    tests = [
        test_health_check,
        test_providers_list,
        test_openai_storytelling,
        test_generic_text_generation
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    print("Test Summary:")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return True
    else:
        print("✗ Some tests failed.")
        return False

if __name__ == "__main__":
    main()