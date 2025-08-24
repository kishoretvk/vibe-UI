from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from cache_manager import CacheManager

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the cache manager
cache_manager = CacheManager()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "cache-service",
        "version": "1.0.0"
    })

# Set cache value endpoint
@app.route('/api/cache', methods=['POST'])
def set_cache():
    try:
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')
        ttl = data.get('ttl')
        tags = data.get('tags', [])
        
        if not key or value is None:
            return jsonify({"error": "Key and value are required"}), 400
        
        if tags:
            success = cache_manager.set_with_tags(key, value, tags, ttl)
        else:
            success = cache_manager.set(key, value, ttl)
        
        if success:
            return jsonify({"message": "Value cached successfully"}), 201
        else:
            return jsonify({"error": "Failed to cache value"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Cache set failed: {str(e)}"}), 500

# Get cache value endpoint
@app.route('/api/cache/<key>', methods=['GET'])
def get_cache(key):
    try:
        value = cache_manager.get(key)
        
        if value is not None:
            return jsonify({"key": key, "value": value}), 200
        else:
            return jsonify({"error": "Key not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Cache get failed: {str(e)}"}), 500

# Delete cache value endpoint
@app.route('/api/cache/<key>', methods=['DELETE'])
def delete_cache(key):
    try:
        success = cache_manager.delete(key)
        
        if success:
            return jsonify({"message": "Value deleted successfully"}), 200
        else:
            return jsonify({"error": "Key not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Cache delete failed: {str(e)}"}), 500

# Check if key exists endpoint
@app.route('/api/cache/<key>/exists', methods=['GET'])
def exists_cache(key):
    try:
        exists = cache_manager.exists(key)
        return jsonify({"key": key, "exists": exists}), 200
    except Exception as e:
        return jsonify({"error": f"Cache exists check failed: {str(e)}"}), 500

# Invalidate cache by tag endpoint
@app.route('/api/cache/invalidate-tag/<tag>', methods=['DELETE'])
def invalidate_tag(tag):
    try:
        deleted_count = cache_manager.invalidate_tag(tag)
        return jsonify({
            "message": f"Invalidated {deleted_count} entries with tag '{tag}'"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Tag invalidation failed: {str(e)}"}), 500

# Get cache statistics endpoint
@app.route('/api/cache/stats', methods=['GET'])
def get_stats():
    try:
        stats = cache_manager.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": f"Stats retrieval failed: {str(e)}"}), 500

# Flush all cache endpoint
@app.route('/api/cache/flush', methods=['DELETE'])
def flush_cache():
    try:
        success = cache_manager.flush_all()
        if success:
            return jsonify({"message": "Cache flushed successfully"}), 200
        else:
            return jsonify({"error": "Failed to flush cache"}), 500
    except Exception as e:
        return jsonify({"error": f"Cache flush failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=True)