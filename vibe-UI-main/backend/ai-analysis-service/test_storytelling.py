#!/usr/bin/env python3
"""
Test script for AI analysis service storytelling endpoint
"""

import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5001"

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

def test_storytelling():
    """Test the storytelling endpoint"""
    print("\nTesting storytelling endpoint...")
    try:
        # Sample data to send
        sample_data = [
            {"date": "2024-01-01", "category": "Revenue", "amount": 125000},
            {"date": "2024-01-01", "category": "Expense", "amount": 95000},
            {"date": "2024-02-01", "category": "Revenue", "amount": 135000},
            {"date": "2024-02-01", "category": "Expense", "amount": 98000}
        ]
        
        response = requests.post(f"{SERVICE_URL}/api/storytelling", json=sample_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Storytelling successful")
            print(f"  Title: {data.get('title', 'N/A')}")
            print(f"  Summary: {data.get('summary', 'N/A')}")
            print(f"  Insights count: {len(data.get('insights', []))}")
            print(f"  Recommendations count: {len(data.get('recommendations', []))}")
            return True
        else:
            print(f"✗ Storytelling failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Storytelling failed: {e}")
        return False

def main():
    """Main test function"""
    print("AI Analysis Service Storytelling Test")
    print("=" * 40)
    
    # Run tests
    tests = [
        test_health_check,
        test_storytelling
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    print("Test Summary:")
    print("=" * 40)
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