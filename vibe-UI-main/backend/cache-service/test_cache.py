#!/usr/bin/env python3
"""
Test script for cache service
"""

import requests
import json
import time

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5010"

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

def test_set_cache():
    """Test setting a value in cache"""
    print("\nTesting set cache endpoint...")
    try:
        data = {
            "key": "test_key",
            "value": {"name": "Test Data", "value": 123},
            "ttl": 60,
            "tags": ["test", "example"]
        }
        
        response = requests.post(f"{SERVICE_URL}/api/cache", json=data)
        if response.status_code == 201:
            print(f"✓ Set cache successful: {response.json()}")
            return True
        else:
            print(f"✗ Set cache failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Set cache failed: {e}")
        return False

def test_get_cache():
    """Test getting a value from cache"""
    print("\nTesting get cache endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/cache/test_key")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get cache successful: {data}")
            return True
        elif response.status_code == 404:
            print("⚠ Key not found in cache")
            return True
        else:
            print(f"✗ Get cache failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get cache failed: {e}")
        return False

def test_exists_cache():
    """Test checking if a key exists in cache"""
    print("\nTesting exists cache endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/cache/test_key/exists")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Exists cache successful: {data}")
            return True
        else:
            print(f"✗ Exists cache failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Exists cache failed: {e}")
        return False

def test_delete_cache():
    """Test deleting a value from cache"""
    print("\nTesting delete cache endpoint...")
    try:
        response = requests.delete(f"{SERVICE_URL}/api/cache/test_key")
        if response.status_code == 200:
            print(f"✓ Delete cache successful: {response.json()}")
            return True
        elif response.status_code == 404:
            print("⚠ Key not found in cache")
            return True
        else:
            print(f"✗ Delete cache failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Delete cache failed: {e}")
        return False

def test_invalidate_tag():
    """Test invalidating cache by tag"""
    print("\nTesting invalidate tag endpoint...")
    try:
        # First set a value with a tag
        data = {
            "key": "tagged_key",
            "value": {"tagged": "data"},
            "ttl": 60,
            "tags": ["test_tag"]
        }
        requests.post(f"{SERVICE_URL}/api/cache", json=data)
        
        # Then invalidate the tag
        response = requests.delete(f"{SERVICE_URL}/api/cache/invalidate-tag/test_tag")
        if response.status_code == 200:
            print(f"✓ Invalidate tag successful: {response.json()}")
            return True
        else:
            print(f"✗ Invalidate tag failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Invalidate tag failed: {e}")
        return False

def test_cache_stats():
    """Test getting cache statistics"""
    print("\nTesting cache stats endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/cache/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Cache stats successful: {data}")
            return True
        else:
            print(f"✗ Cache stats failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Cache stats failed: {e}")
        return False

def main():
    """Main test function"""
    print("Cache Service Test")
    print("=" * 20)
    
    # Run tests
    tests = [
        test_health_check,
        test_set_cache,
        test_get_cache,
        test_exists_cache,
        test_cache_stats,
        test_invalidate_tag,
        test_delete_cache
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    print("Test Summary:")
    print("=" * 20)
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