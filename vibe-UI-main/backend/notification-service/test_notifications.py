"""
Test script for notification service
"""
import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5004"

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

def test_create_email_notification():
    """Test creating an email notification"""
    print("\nTesting create email notification endpoint...")
    try:
        data = {
            "type": "email",
            "recipients": ["user@example.com"],
            "subject": "Test Notification",
            "message": "This is a test notification from the notification service."
        }
        
        response = requests.post(f"{SERVICE_URL}/api/notifications", json=data)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Create email notification successful: Notification ID {data.get('id')}")
            print(f"  Status: {data.get('status')}")
            return True
        else:
            print(f"✗ Create email notification failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Create email notification failed: {e}")
        return False

def test_get_notifications():
    """Test getting all notifications"""
    print("\nTesting get notifications endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/notifications")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get notifications successful: {len(data)} notifications found")
            return True
        else:
            print(f"✗ Get notifications failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get notifications failed: {e}")
        return False

def test_get_notification():
    """Test getting a specific notification"""
    print("\nTesting get notification endpoint...")
    try:
        # First create a notification to test with
        create_data = {
            "type": "email",
            "recipients": ["user@example.com"],
            "subject": "Test Notification",
            "message": "This is a test notification."
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/notifications", json=create_data)
        if create_response.status_code == 201:
            created_notification = create_response.json()
            notification_id = created_notification['id']
            
            # Now get the notification
            response = requests.get(f"{SERVICE_URL}/api/notifications/{notification_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Get notification successful: {data.get('subject')}")
                return True
            else:
                print(f"✗ Get notification failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create notification for testing")
            return False
    except Exception as e:
        print(f"✗ Get notification failed: {e}")
        return False

def test_update_notification():
    """Test updating a notification"""
    print("\nTesting update notification endpoint...")
    try:
        # First create a notification to test with
        create_data = {
            "type": "email",
            "recipients": ["user@example.com"],
            "subject": "Test Notification",
            "message": "This is a test notification."
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/notifications", json=create_data)
        if create_response.status_code == 201:
            created_notification = create_response.json()
            notification_id = created_notification['id']
            
            # Now update the notification
            update_data = {
                "subject": "Updated Test Notification",
                "message": "This is an updated test notification."
            }
            
            response = requests.put(f"{SERVICE_URL}/api/notifications/{notification_id}", json=update_data)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Update notification successful: Subject changed to {data.get('subject')}")
                return True
            else:
                print(f"✗ Update notification failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create notification for testing")
            return False
    except Exception as e:
        print(f"✗ Update notification failed: {e}")
        return False

def test_delete_notification():
    """Test deleting a notification"""
    print("\nTesting delete notification endpoint...")
    try:
        # First create a notification to test with
        create_data = {
            "type": "email",
            "recipients": ["user@example.com"],
            "subject": "Test Notification",
            "message": "This is a test notification."
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/notifications", json=create_data)
        if create_response.status_code == 201:
            created_notification = create_response.json()
            notification_id = created_notification['id']
            
            # Now delete the notification
            response = requests.delete(f"{SERVICE_URL}/api/notifications/{notification_id}")
            if response.status_code == 200:
                print(f"✓ Delete notification successful")
                return True
            else:
                print(f"✗ Delete notification failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        else:
            print(f"✗ Failed to create notification for testing")
            return False
    except Exception as e:
        print(f"✗ Delete notification failed: {e}")
        return False

def main():
    """Main test function"""
    print("Notification Service Test")
    print("=" * 20)
    
    # Run tests
    tests = [
        test_health_check,
        test_create_email_notification,
        test_get_notifications,
        test_get_notification,
        test_update_notification,
        test_delete_notification
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