#!/usr/bin/env python3
"""
Test script to verify the new microservices architecture
"""

import requests
import time
import json

def test_data_generator_service():
    """Test the data generator service"""
    print("Testing Data Generator Service...")
    try:
        response = requests.get("http://localhost:5009/api/data")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Data Generator Service is running. Returned {len(data)} records.")
            return True
        else:
            print(f"✗ Data Generator Service returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Data Generator Service is not running or not accessible")
        return False
    except Exception as e:
        print(f"✗ Error testing Data Generator Service: {e}")
        return False

def test_ai_analysis_service():
    """Test the AI analysis service"""
    print("Testing AI Analysis Service...")
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5001/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ AI Analysis Service is running. Status: {data['status']}")
            
            # Test storytelling endpoint
            sample_data = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
            story_response = requests.post("http://localhost:5001/api/storytelling", json=sample_data)
            if story_response.status_code == 200:
                print("✓ AI Analysis Service storytelling endpoint is working")
                return True
            else:
                print(f"✗ AI Analysis Service storytelling endpoint returned status code {story_response.status_code}")
                return False
        else:
            print(f"✗ AI Analysis Service health check returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ AI Analysis Service is not running or not accessible")
        return False
    except Exception as e:
        print(f"✗ Error testing AI Analysis Service: {e}")
        return False

def test_data_processing_service():
    """Test the data processing service"""
    print("Testing Data Processing Service...")
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5002/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Data Processing Service is running. Status: {data['status']}")
            
            # Test validation endpoint
            sample_data = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
            validation_response = requests.post("http://localhost:5002/api/validate", json=sample_data)
            if validation_response.status_code == 200:
                print("✓ Data Processing Service validation endpoint is working")
                return True
            else:
                print(f"✗ Data Processing Service validation endpoint returned status code {validation_response.status_code}")
                return False
        else:
            print(f"✗ Data Processing Service health check returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Data Processing Service is not running or not accessible")
        return False
    except Exception as e:
        print(f"✗ Error testing Data Processing Service: {e}")
        return False

def main():
    """Main test function"""
    print("Vibe-UI Architecture Test")
    print("=" * 30)
    
    # Test each service
    services = [
        test_data_generator_service,
        test_ai_analysis_service,
        test_data_processing_service
    ]
    
    results = []
    for service_test in services:
        result = service_test()
        results.append(result)
        print()
    
    # Summary
    print("Test Summary:")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All services are running correctly!")
        return True
    else:
        print("✗ Some services are not running correctly.")
        return False

if __name__ == "__main__":
    main()