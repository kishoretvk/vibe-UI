from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from storytelling_engine import StorytellingEngine

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "ai-analysis-service",
        "version": "1.0.0"
    })

# Basic storytelling endpoint
@app.route('/api/storytelling', methods=['POST'])
def generate_story():
    data = request.get_json()
    
    # Use storytelling engine
    engine = StorytellingEngine()
    story = engine.analyze_data(data or [])
    
    return jsonify(story)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)