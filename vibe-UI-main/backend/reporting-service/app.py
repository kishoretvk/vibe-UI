from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import io
from report_generator import report_generator

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "reporting-service",
        "version": "1.0.0"
    })

# Get all report templates
@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = report_generator.get_templates()
    return jsonify(templates)

# Get specific report template
@app.route('/api/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    template = report_generator.get_template(template_id)
    if not template:
        return jsonify({"error": "Template not found"}), 404
    return jsonify(template)

# Generate report from template
@app.route('/api/reports/generate', methods=['POST'])
def generate_report():
    data = request.get_json()
    
    template_id = data.get("template_id")
    data_sources = data.get("data_sources", {})
    parameters = data.get("parameters", {})
    
    if not template_id:
        return jsonify({"error": "template_id is required"}), 400
    
    try:
        report = report_generator.create_report_from_template(template_id, data_sources, parameters)
        return jsonify(report)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

# Get all reports endpoint
@app.route('/api/reports', methods=['GET'])
def get_reports():
    # Placeholder for actual implementation
    reports = [
        {
            "id": "1",
            "title": "Sales Report",
            "description": "Monthly sales report",
            "created_at": "2023-01-15T10:30:00Z",
            "updated_at": "2023-01-15T10:30:00Z"
        },
        {
            "id": "2",
            "title": "User Engagement Report",
            "description": "Weekly user engagement metrics",
            "created_at": "2023-01-14T09:15:00Z",
            "updated_at": "2023-01-14T09:15:00Z"
        }
    ]
    return jsonify(reports)

# Get specific report endpoint
@app.route('/api/reports/<report_id>', methods=['GET'])
def get_report(report_id):
    # Placeholder for actual implementation
    report = {
        "id": report_id,
        "title": "Sample Report",
        "description": "This is a sample report",
        "data": [
            {"month": "January", "value": 100},
            {"month": "February", "value": 120},
            {"month": "March", "value": 140}
        ],
        "created_at": "2023-01-15T10:30:00Z",
        "updated_at": "2023-01-15T10:30:00Z"
    }
    return jsonify(report)

# Create new report endpoint
@app.route('/api/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    
    # Placeholder for actual implementation
    new_report = {
        "id": "3",
        "title": data.get("title", "Untitled Report"),
        "description": data.get("description", ""),
        "created_at": "2023-01-16T10:30:00Z",
        "updated_at": "2023-01-16T10:30:00Z"
    }
    return jsonify(new_report), 201

# Update report endpoint
@app.route('/api/reports/<report_id>', methods=['PUT'])
def update_report(report_id):
    data = request.get_json()
    
    # Placeholder for actual implementation
    updated_report = {
        "id": report_id,
        "title": data.get("title", "Untitled Report"),
        "description": data.get("description", ""),
        "created_at": "2023-01-15T10:30:00Z",
        "updated_at": "2023-01-16T10:30:00Z"
    }
    return jsonify(updated_report)

# Delete report endpoint
@app.route('/api/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    # Placeholder for actual implementation
    return jsonify({"message": f"Report {report_id} deleted successfully"})

# Export report endpoint
@app.route('/api/reports/<report_id>/export', methods=['GET'])
def export_report(report_id):
    format = request.args.get('format', 'json')
    
    # Placeholder for actual implementation - in a real app, you would fetch the report by ID
    # For now, we'll create a sample report
    sample_report = {
        "id": report_id,
        "title": "Sample Report",
        "description": "This is a sample report",
        "created_at": "2023-01-15T10:30:00Z",
        "sections": [
            {
                "title": "Sample Data",
                "type": "table",
                "data": [
                    {"name": "Item 1", "value": 100},
                    {"name": "Item 2", "value": 200},
                    {"name": "Item 3", "value": 300}
                ]
            }
        ]
    }
    
    try:
        exported_data = report_generator.export_report(sample_report, format)
        
        # Create a file-like object
        file_data = io.BytesIO(exported_data)
        file_data.seek(0)
        
        # Return the file
        if format.lower() == "json":
            return send_file(
                file_data,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'report_{report_id}.json'
            )
        elif format.lower() == "csv":
            return send_file(
                file_data,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'report_{report_id}.csv'
            )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to export report: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)