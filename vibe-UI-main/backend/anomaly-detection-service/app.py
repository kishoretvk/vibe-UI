from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from anomaly_detector import AnomalyDetector

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize the anomaly detector
detector = AnomalyDetector()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "anomaly-detection-service",
        "version": "1.0.0",
        "available_methods": detector.get_detection_methods()
    })

# Get available detection methods
@app.route('/api/methods', methods=['GET'])
def get_methods():
    return jsonify({
        "methods": detector.get_detection_methods()
    })

# Detect anomalies endpoint
@app.route('/api/detect', methods=['POST'])
def detect_anomalies():
    try:
        data = request.get_json()
        
        # Extract data and parameters
        records = data.get('data', [])
        method = data.get('method', 'isolation_forest')
        
        if not records:
            return jsonify({"error": "No data provided"}), 400
        
        # Validate method
        available_methods = detector.get_detection_methods()
        if method not in available_methods:
            return jsonify({
                "error": f"Invalid method. Available methods: {available_methods}"
            }), 400
        
        # Detect anomalies
        results = detector.detect_anomalies(records, method)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": f"Anomaly detection failed: {str(e)}"}), 500

# Quick anomaly detection with default method
@app.route('/api/quick-detect', methods=['POST'])
def quick_detect():
    try:
        data = request.get_json()
        records = data.get('data', [])
        
        if not records:
            return jsonify({"error": "No data provided"}), 400
        
        # Use default method (isolation forest)
        results = detector.detect_anomalies(records)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": f"Quick anomaly detection failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5006))
    app.run(host='0.0.0.0', port=port, debug=True)