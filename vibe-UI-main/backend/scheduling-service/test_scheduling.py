"""
Test script for scheduling service
"""
import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5007"

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

def test_create_schedule():
    """Test creating a scheduled report"""
    print("\nTesting create schedule endpoint...")
    try:
        data = {
            "report_template_id": "sales_summary",
            "schedule_frequency": "daily",
            "schedule_time": "09:00",
            "destination": "email",
            "recipients": ["user@example.com"],
            "parameters": {
                "date_range": "last_30_days"
            },
            "enabled": True
        }
        
        response = requests.post(f"{SERVICE_URL}/api/schedules", json=data)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Create schedule successful: Schedule ID {data.get('id')}")
            return True
        else:
            print(f"✗ Create schedule failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Create schedule failed: {e}")
        return False

def test_get_schedules():
    """Test getting all scheduled reports"""
    print("\nTesting get schedules endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/schedules")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get schedules successful: {len(data)} schedules found")
            return True
        else:
            print(f"✗ Get schedules failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get schedules failed: {e}")
        return False

def test_get_schedule():
    """Test getting a specific scheduled report"""
    print("\nTesting get schedule endpoint...")
    try:
        # First create a schedule to test with
        create_data = {
            "report_template_id": "user_engagement",
            "schedule_frequency": "weekly",
            "schedule_time": "10:00",
            "destination": "file",
            "recipients": [],
            "parameters": {
                "date_range": "last_7_days"
            },
            "enabled": True
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/schedules", json=create_data)
        if create_response.status_code == 201:
            created_schedule = create_response.json()
            schedule_id = created_schedule['id']
            
            # Now get the schedule
            response = requests.get(f"{SERVICE_URL}/api/schedules/{schedule_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Get schedule successful: {data.get('report_template_id')}")
                return True
            else:
                print(f"✗ Get schedule failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create schedule for testing")
            return False
    except Exception as e:
        print(f"✗ Get schedule failed: {e}")
        return False

def test_update_schedule():
    """Test updating a scheduled report"""
    print("\nTesting update schedule endpoint...")
    try:
        # First create a schedule to test with
        create_data = {
            "report_template_id": "user_engagement",
            "schedule_frequency": "weekly",
            "schedule_time": "10:00",
            "destination": "file",
            "recipients": [],
            "parameters": {
                "date_range": "last_7_days"
            },
            "enabled": True
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/schedules", json=create_data)
        if create_response.status_code == 201:
            created_schedule = create_response.json()
            schedule_id = created_schedule['id']
            
            # Now update the schedule
            update_data = {
                "schedule_frequency": "monthly",
                "schedule_time": "14:00",
                "enabled": False
            }
            
            response = requests.put(f"{SERVICE_URL}/api/schedules/{schedule_id}", json=update_data)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Update schedule successful: Frequency changed to {data.get('schedule_frequency')}")
                return True
            else:
                print(f"✗ Update schedule failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create schedule for testing")
            return False
    except Exception as e:
        print(f"✗ Update schedule failed: {e}")
        return False

def test_delete_schedule():
    """Test deleting a scheduled report"""
    print("\nTesting delete schedule endpoint...")
    try:
        # First create a schedule to test with
        create_data = {
            "report_template_id": "user_engagement",
            "schedule_frequency": "weekly",
            "schedule_time": "10:00",
            "destination": "file",
            "recipients": [],
            "parameters": {
                "date_range": "last_7_days"
            },
            "enabled": True
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/schedules", json=create_data)
        if create_response.status_code == 201:
            created_schedule = create_response.json()
            schedule_id = created_schedule['id']
            
            # Now delete the schedule
            response = requests.delete(f"{SERVICE_URL}/api/schedules/{schedule_id}")
            if response.status_code == 200:
                print(f"✓ Delete schedule successful")
                return True
            else:
                print(f"✗ Delete schedule failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create schedule for testing")
            return False
    except Exception as e:
        print(f"✗ Delete schedule failed: {e}")
        return False

def main():
    """Main test function"""
    print("Scheduling Service Test")
    print("=" * 20)
    
    # Run tests
    tests = [
        test_health_check,
        test_create_schedule,
        test_get_schedules,
        test_get_schedule,
        test_update_schedule,
        test_delete_schedule
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