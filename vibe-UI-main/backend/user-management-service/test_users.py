"""
Test script for user management service
"""
import requests
import json

# Service URL (adjust if running on different host/port)
SERVICE_URL = "http://localhost:5008"

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

def test_create_user():
    """Test creating a new user"""
    print("\nTesting create user endpoint...")
    try:
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "role": "user"
        }
        
        response = requests.post(f"{SERVICE_URL}/api/users", json=data)
        if response.status_code == 201:
            data = response.json()
            print(f"✓ Create user successful: User ID {data.get('id')}")
            print(f"  Username: {data.get('username')}")
            return True
        elif response.status_code == 409:
            print("⚠ User already exists")
            return True
        else:
            print(f"✗ Create user failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Create user failed: {e}")
        return False

def test_get_users():
    """Test getting all users"""
    print("\nTesting get users endpoint...")
    try:
        response = requests.get(f"{SERVICE_URL}/api/users")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Get users successful: {len(data)} users found")
            return True
        else:
            print(f"✗ Get users failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Get users failed: {e}")
        return False

def test_get_user():
    """Test getting a specific user"""
    print("\nTesting get user endpoint...")
    try:
        # First create a user to test with
        create_data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpassword123",
            "first_name": "Test2",
            "last_name": "User2"
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/users", json=create_data)
        if create_response.status_code == 201 or create_response.status_code == 409:
            # Now get all users to find the user ID
            get_response = requests.get(f"{SERVICE_URL}/api/users")
            if get_response.status_code == 200:
                users = get_response.json()
                user_id = None
                for user in users:
                    if user['username'] == 'testuser2':
                        user_id = user['id']
                        break
                
                if user_id:
                    # Now get the specific user
                    response = requests.get(f"{SERVICE_URL}/api/users/{user_id}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✓ Get user successful: {data.get('username')}")
                        return True
                    else:
                        print(f"✗ Get user failed with status {response.status_code}")
                        print(f"  Response: {response.text}")
                        return False
                else:
                    print("✗ Could not find user ID")
                    return False
            else:
                print(f"✗ Failed to get users for testing")
                return False
        else:
            print(f"✗ Failed to create user for testing")
            return False
    except Exception as e:
        print(f"✗ Get user failed: {e}")
        return False

def test_update_user():
    """Test updating a user"""
    print("\nTesting update user endpoint...")
    try:
        # First create a user to test with
        create_data = {
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "testpassword123",
            "first_name": "Test3",
            "last_name": "User3"
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/users", json=create_data)
        if create_response.status_code == 201 or create_response.status_code == 409:
            # Now get all users to find the user ID
            get_response = requests.get(f"{SERVICE_URL}/api/users")
            if get_response.status_code == 200:
                users = get_response.json()
                user_id = None
                for user in users:
                    if user['username'] == 'testuser3':
                        user_id = user['id']
                        break
                
                if user_id:
                    # Now update the user
                    update_data = {
                        "first_name": "UpdatedTest3",
                        "last_name": "UpdatedUser3"
                    }
                    
                    response = requests.put(f"{SERVICE_URL}/api/users/{user_id}", json=update_data)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✓ Update user successful: Name changed to {data.get('first_name')} {data.get('last_name')}")
                        return True
                    else:
                        print(f"✗ Update user failed with status {response.status_code}")
                        print(f"  Response: {response.text}")
                        return False
                else:
                    print("✗ Could not find user ID")
                    return False
            else:
                print(f"✗ Failed to get users for testing")
                return False
        else:
            print(f"✗ Failed to create user for testing")
            return False
    except Exception as e:
        print(f"✗ Update user failed: {e}")
        return False

def test_delete_user():
    """Test deleting a user"""
    print("\nTesting delete user endpoint...")
    try:
        # First create a user to test with
        create_data = {
            "username": "testuser4",
            "email": "testuser4@example.com",
            "password": "testpassword123",
            "first_name": "Test4",
            "last_name": "User4"
        }
        
        create_response = requests.post(f"{SERVICE_URL}/api/users", json=create_data)
        if create_response.status_code == 201:
            created_user = create_response.json()
            user_id = created_user['id']
            
            # Now delete the user
            response = requests.delete(f"{SERVICE_URL}/api/users/{user_id}")
            if response.status_code == 200:
                print(f"✓ Delete user successful")
                return True
            else:
                print(f"✗ Delete user failed with status {response.status_code}")
                print(f"  Response: {response.text}")
                return False
        elif create_response.status_code == 409:
            print("⚠ User already exists, skipping delete test")
            return True
        else:
            print(f"✗ Failed to create user for testing")
            return False
    except Exception as e:
        print(f"✗ Delete user failed: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login endpoint...")
    try:
        data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{SERVICE_URL}/api/auth/login", json=data)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Login successful: {data.get('username')}")
            print(f"  Token: {data.get('token', 'Not provided')[:20]}...")
            return True
        else:
            print(f"✗ Login failed with status {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return False

def main():
    """Main test function"""
    print("User Management Service Test")
    print("=" * 20)
    
    # Run tests
    tests = [
        test_health_check,
        test_create_user,
        test_get_users,
        test_get_user,
        test_update_user,
        test_delete_user,
        test_login
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