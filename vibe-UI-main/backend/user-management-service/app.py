from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
import hashlib
import jwt
import datetime as dt

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Secret key for JWT (in a real app, this should be loaded from environment variables)
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')

# In-memory storage for users (in a real app, this would be a database)
users = {}
user_id_counter = 1

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "user-management-service",
        "version": "1.0.0"
    })

# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    # Return users without passwords
    users_without_passwords = []
    for user in users.values():
        user_copy = user.copy()
        del user_copy['password']
        users_without_passwords.append(user_copy)
    return jsonify(users_without_passwords)

# Get specific user
@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_id = int(user_id)
    if user_id in users:
        user = users[user_id].copy()
        del user['password']  # Don't return password
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# Create new user
@app.route('/api/users', methods=['POST'])
def create_user():
    global user_id_counter
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Check if user already exists
    for user in users.values():
        if user['username'] == data['username'] or user['email'] == data['email']:
            return jsonify({"error": "User with this username or email already exists"}), 409
    
    # Hash password
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    # Create new user
    new_user = {
        "id": user_id_counter,
        "username": data['username'],
        "email": data['email'],
        "password": hashed_password,
        "first_name": data.get('first_name', ''),
        "last_name": data.get('last_name', ''),
        "role": data.get('role', 'user'),  # user, admin
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    users[user_id_counter] = new_user
    user_id_counter += 1
    
    # Return user without password
    user_response = new_user.copy()
    del user_response['password']
    
    return jsonify(user_response), 201

# Update user
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_id = int(user_id)
    
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    
    # Update user
    user = users[user_id]
    
    # Updateable fields (password handled separately)
    updatable_fields = ['email', 'first_name', 'last_name', 'role']
    for field in updatable_fields:
        if field in data:
            user[field] = data[field]
    
    # Handle password update
    if 'password' in data:
        user['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user['updated_at'] = datetime.now().isoformat()
    
    # Return user without password
    user_response = user.copy()
    del user_response['password']
    
    return jsonify(user_response)

# Delete user
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_id = int(user_id)
    
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    del users[user_id]
    return jsonify({"message": "User deleted successfully"})

# User login
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    # Hash password for comparison
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    # Find user
    user = None
    for u in users.values():
        if u['username'] == data['username'] and u['password'] == hashed_password:
            user = u
            break
    
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Update last login
    user['last_login'] = datetime.now().isoformat()
    
    # Generate JWT token
    payload = {
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': dt.datetime.utcnow() + dt.timedelta(hours=24)  # Token expires in 24 hours
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    # Return user without password and with token
    user_response = user.copy()
    del user_response['password']
    user_response['token'] = token
    
    return jsonify(user_response)

# User logout
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    # In a real implementation, you would invalidate the token
    # For now, we'll just return a success message
    return jsonify({"message": "Logged out successfully"})

# Get current user profile
@app.route('/api/profile', methods=['GET'])
def get_profile():
    # In a real implementation, you would extract user ID from JWT token
    # For now, we'll just return a placeholder
    return jsonify({"message": "User profile endpoint - implementation pending"})

if __name__ == '__main__':
    # Create a default admin user for testing
    admin_user = {
        "id": user_id_counter,
        "username": "admin",
        "email": "admin@example.com",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "last_login": None
    }
    users[user_id_counter] = admin_user
    user_id_counter += 1
    
    port = int(os.environ.get('PORT', 5008))
    app.run(host='0.0.0.0', port=port, debug=True)