"""
Test script for reporting service
"""
import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5003"

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

def test_get_templates():
    """Test getting report templates"""
    print("\nTesting get templates endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/templates")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get templates successful: {len(data)} templates found")
            return True
        else:
            print(f"✗ Get templates failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get templates failed: {e}")
        return False

def test_get_template():
    """Test getting a specific template"""
    print("\nTesting get template endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/templates/sales_summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get template successful: {data.get('name', 'Unknown')}")
            return True
        elif response.status_code == 404:
            print("⚠ Template not found")
            return True
        else:
            print(f"✗ Get template failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get template failed: {e}")
        return False

def test_generate_report():
    """Test generating a report from template"""
    print("\nTesting generate report endpoint...")
    try:
        data = {
            "template_id": "sales_summary",
            "data_sources": {
                "sales_data": [
                    {"month": "January", "sales": 10000},
                    {"month": "February", "sales": 12000},
                    {"month": "March", "sales": 15000}
                ],
                "product_data": [
                    {"product": "Product A", "sales": 5000},
                    {"product": "Product B", "sales": 7000},
                    {"product": "Product C", "sales": 8000}
                ]
            }
        }
        
        response = requests.post(f"{SERVICE_URL}/api/reports/generate", json=data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Generate report successful: {data.get('title', 'Unknown')}")
            return True
        else:
            print(f"✗ Generate report failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Generate report failed: {e}")
        return False

def test_generate_parameterized_report():
    """Test generating a parameterized report"""
    print("\nTesting generate parameterized report endpoint...")
    try:
        data = {
            "template_id": "sales_summary",
            "parameters": {
                "date_range": "2023-01-01_to_2023-03-31",
                "region": "North America"
            },
            "data_sources": {
                "sales_data": [
                    {"month": "January", "sales": 10000},
                    {"month": "February", "sales": 12000},
                    {"month": "March", "sales": 15000}
                ],
                "product_data": [
                    {"product": "Product A", "sales": 5000},
                    {"product": "Product B", "sales": 7000},
                    {"product": "Product C", "sales": 8000}
                ]
            }
        }
        
        response = requests.post(f"{SERVICE_URL}/api/reports/generate", json=data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Generate parameterized report successful: {data.get('title', 'Unknown')}")
            print(f"  Parameters: {data.get('parameters', {})}")
            return True
        else:
            print(f"✗ Generate parameterized report failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Generate parameterized report failed: {e}")
        return False

def main():
    """Main test function"""
    print("Reporting Service Test")
    print("=" * 20)
    
    # Run tests
    tests = [
        test_health_check,
        test_get_templates,
        test_get_template,
        test_generate_report,
        test_generate_parameterized_report
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