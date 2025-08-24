from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from llm_provider import LLMProviderFactory
from providers import OpenAIProvider, GeminiProvider, OllamaProvider
from openai_integration import OpenAIIntegration

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "llm-integration-service",
        "version": "1.0.0",
        "available_providers": LLMProviderFactory.get_available_providers()
    })

# Get available providers
@app.route('/api/providers', methods=['GET'])
def get_providers():
    return jsonify({
        "providers": LLMProviderFactory.get_available_providers()
    })

# Generate text using a specific provider
@app.route('/api/generate', methods=['POST'])
def generate_text():
    try:
        data = request.get_json()
        provider_name = data.get('provider')
        prompt = data.get('prompt')
        config = data.get('config', {})
        generation_params = data.get('params', {})
        
        if not provider_name or not prompt:
            return jsonify({"error": "Provider and prompt are required"}), 400
        
        # Create provider instance
        provider = LLMProviderFactory.create_provider(provider_name, config)
        
        # Generate text
        result = provider.generate_text(prompt, **generation_params)
        
        return jsonify({
            "result": result,
            "model_info": provider.get_model_info()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate embedding using a specific provider
@app.route('/api/embed', methods=['POST'])
def generate_embedding():
    try:
        data = request.get_json()
        provider_name = data.get('provider')
        text = data.get('text')
        config = data.get('config', {})
        
        if not provider_name or not text:
            return jsonify({"error": "Provider and text are required"}), 400
        
        # Create provider instance
        provider = LLMProviderFactory.create_provider(provider_name, config)
        
        # Generate embedding
        embedding = provider.generate_embedding(text)
        
        return jsonify({
            "embedding": embedding,
            "model_info": provider.get_model_info()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate storytelling insights using OpenAI
@app.route('/api/storytelling', methods=['POST'])
def generate_storytelling():
    try:
        data = request.get_json()
        data_description = data.get('data_description')
        data_sample = data.get('data_sample', '')
        
        if not data_description:
            return jsonify({"error": "Data description is required"}), 400
        
        # Use OpenAI integration
        openai_client = OpenAIIntegration()
        insights = openai_client.generate_storytelling_insights(data_description, data_sample)
        
        return jsonify({
            "insights": insights,
            "model_info": openai_client.get_model_info()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generate chart description using OpenAI
@app.route('/api/chart-description', methods=['POST'])
def generate_chart_description():
    try:
        data = request.get_json()
        data_description = data.get('data_description')
        chart_type = data.get('chart_type')
        
        if not data_description or not chart_type:
            return jsonify({"error": "Data description and chart type are required"}), 400
        
        # Use OpenAI integration
        openai_client = OpenAIIntegration()
        description = openai_client.generate_chart_description(data_description, chart_type)
        
        return jsonify({
            "description": description,
            "model_info": openai_client.get_model_info()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    app.run(host='0.0.0.0', port=port, debug=True)