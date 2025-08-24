from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys
import requests
import hashlib
import json
sys.path.append(os.path.dirname(__file__))
from data_connectors import create_connector

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "data-processing-service",
        "version": "1.0.0"
    })

# Data validation endpoint
@app.route('/api/validate', methods=['POST'])
def validate_data():
    data = request.get_json()
    
    # Placeholder for actual data validation logic
    validation_result = {
        "valid": True,
        "rowCount": len(data) if isinstance(data, list) else 0,
        "columns": list(data[0].keys()) if isinstance(data, list) and len(data) > 0 else [],
        "issues": []
    }
    
    return jsonify(validation_result)

# Data transformation endpoint
@app.route('/api/transform', methods=['POST'])
def transform_data():
    data = request.get_json()
    
    # Placeholder for actual data transformation logic
    transformed_data = {
        "data": data,
        "transformationsApplied": ["none"],
        "rowCount": len(data) if isinstance(data, list) else 0
    }
    
    return jsonify(transformed_data)

# Data connector endpoint
@app.route('/api/connect', methods=['POST'])
def connect_to_data_source():
    config = request.get_json()
    
    if not config or 'type' not in config:
        return jsonify({"error": "Missing connector type in request"}), 400
    
    try:
        connector_type = config['type']
        connector_params = config.get('params', {})
        
        # Get cache service URL from environment
        cache_service_url = os.getenv('CACHE_SERVICE_URL', 'http://cache-service:5005')
        
        # Generate cache key based on config
        cache_key_data = {
            "type": connector_type,
            "params": connector_params,
            "query": config.get('query', '')
        }
        cache_key = hashlib.md5(json.dumps(cache_key_data, sort_keys=True).encode()).hexdigest()
        cache_key = f"data_connector:{cache_key}"
        
        # Try to get data from cache first
        try:
            cache_response = requests.get(f"{cache_service_url}/api/cache/{cache_key}", timeout=5)
            if cache_response.status_code == 200:
                cached_data = cache_response.json()
                return jsonify({
                    "success": True,
                    "data": cached_data['value']['data'],
                    "rowCount": cached_data['value']['rowCount'],
                    "cached": True
                })
        except Exception as cache_error:
            # Cache service unavailable, continue with normal flow
            pass
        
        # Create connector
        connector = create_connector(connector_type, **connector_params)
        
        # Connect to data source
        if not connector.connect():
            return jsonify({"error": "Failed to connect to data source"}), 500
        
        # Fetch data if query is provided
        query = config.get('query')
        if query:
            data = connector.fetch_data(query)
        else:
            # For CSV, fetch all data
            if connector_type.lower() == 'csv':
                data = connector.fetch_data()
            else:
                data = []
        
        # Close connection
        connector.disconnect()
        
        # Cache the result for 5 minutes
        try:
            cache_data = {
                "data": data,
                "rowCount": len(data)
            }
            cache_request = {
                "key": cache_key,
                "value": cache_data,
                "ttl": 300  # 5 minutes
            }
            requests.post(f"{cache_service_url}/api/cache", json=cache_request, timeout=5)
        except Exception as cache_error:
            # Cache service unavailable, but we still return the data
            pass
        
        return jsonify({
            "success": True,
            "data": data,
            "rowCount": len(data),
            "cached": False
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)