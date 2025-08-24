#!/usr/bin/env python3
"""
Test script for anomaly detection service
"""

import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5006"

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

def test_detection_methods():
    """Test the detection methods endpoint"""
    print("\nTesting detection methods endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/methods")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Detection methods successful: {data}")
            return True
        else:
            print(f"✗ Detection methods failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Detection methods failed: {e}")
        return False

def test_anomaly_detection():
    """Test the anomaly detection endpoint"""
    print("\nTesting anomaly detection endpoint...")
    try:
        # Sample data with some obvious anomalies
        sample_data = [
            {"id": 1, "value": 100, "category": "A"},
            {"id": 2, "value": 105, "category": "A"},
            {"id": 3, "value": 98, "category": "A"},
            {"id": 4, "value": 102, "category": "A"},
            {"id": 5, "value": 1000, "category": "A"},  # Clear anomaly
            {"id": 6, "value": 99, "category": "A"},
            {"id": 7, "value": 101, "category": "A"},
            {"id": 8, "value": 5, "category": "A"},     # Clear anomaly
            {"id": 9, "value": 103, "category": "A"},
            {"id": 10, "value": 97, "category": "A"}
        ]
        
        # Test with isolation forest
        response = requests.post(f"{SERVICE_URL}/api/detect", json={
            "data": sample_data,
            "method": "isolation_forest"
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Anomaly detection (isolation forest) successful")
            print(f"  Summary: {data.get('summary', 'N/A')}")
            print(f"  Anomalies found: {data.get('anomaly_count', 0)}")
            return True
        else:
            print(f"✗ Anomaly detection failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Anomaly detection failed: {e}")
        return False

def test_quick_detection():
    """Test the quick detection endpoint"""
    print("\nTesting quick detection endpoint...")
    try:
        # Sample data with some obvious anomalies
        sample_data = [
            {"id": 1, "value": 100, "category": "A"},
            {"id": 2, "value": 105, "category": "A"},
            {"id": 3, "value": 98, "category": "A"},
            {"id": 4, "value": 1000, "category": "A"},  # Clear anomaly
            {"id": 5, "value": 99, "category": "A"}
        ]
        
        response = requests.post(f"{SERVICE_URL}/api/quick-detect", json={
            "data": sample_data
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Quick detection successful")
            print(f"  Summary: {data.get('summary', 'N/A')}")
            print(f"  Anomalies found: {data.get('anomaly_count', 0)}")
            return True
        else:
            print(f"✗ Quick detection failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Quick detection failed: {e}")
        return False

def main():
    """Main test function"""
    print("Anomaly Detection Service Test")
    print("=" * 30)
    
    # Run tests
    tests = [
        test_health_check,
        test_detection_methods,
        test_anomaly_detection,
        test_quick_detection
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