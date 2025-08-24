"""
Report generation module for the reporting service
"""
import json
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd

class ReportGenerator:
    """Class to handle report generation"""
    
    def __init__(self):
        self.templates = {}
        self.load_default_templates()
    
    def load_default_templates(self):
        """Load default report templates"""
        self.templates = {
            "sales_summary": {
                "name": "Sales Summary Report",
                "description": "Summary of sales performance",
                "parameters": [
                    {
                        "name": "date_range",
                        "type": "date_range",
                        "required": False,
                        "default": "last_30_days"
                    },
                    {
                        "name": "region",
                        "type": "string",
                        "required": False,
                        "default": "all"
                    }
                ],
                "sections": [
                    {
                        "title": "Executive Summary",
                        "type": "text",
                        "content": "This report summarizes sales performance for the selected period."
                    },
                    {
                        "title": "Sales by Month",
                        "type": "chart",
                        "chart_type": "bar",
                        "data_source": "sales_data"
                    },
                    {
                        "title": "Top Performing Products",
                        "type": "table",
                        "data_source": "product_data"
                    }
                ]
            },
            "user_engagement": {
                "name": "User Engagement Report",
                "description": "Analysis of user engagement metrics",
                "parameters": [
                    {
                        "name": "date_range",
                        "type": "date_range",
                        "required": False,
                        "default": "last_7_days"
                    },
                    {
                        "name": "user_segment",
                        "type": "string",
                        "required": False,
                        "default": "all"
                    }
                ],
                "sections": [
                    {
                        "title": "Engagement Overview",
                        "type": "text",
                        "content": "This report analyzes user engagement metrics over time."
                    },
                    {
                        "title": "Daily Active Users",
                        "type": "chart",
                        "chart_type": "line",
                        "data_source": "user_data"
                    },
                    {
                        "title": "Feature Usage",
                        "type": "chart",
                        "chart_type": "pie",
                        "data_source": "feature_data"
                    }
                ]
            }
        }
    
    def get_templates(self) -> Dict:
        """Get all available report templates"""
        return self.templates
    
    def get_template(self, template_id: str) -> Dict:
        """Get a specific report template"""
        return self.templates.get(template_id, {})
    
    def validate_parameters(self, template_id: str, parameters: Dict) -> Dict:
        """Validate parameters against template requirements"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        validated_params = {}
        template_params = template.get("parameters", [])
        
        # Validate each parameter
        for param in template_params:
            param_name = param["name"]
            param_type = param["type"]
            is_required = param.get("required", False)
            default_value = param.get("default")
            
            # Check if parameter is provided
            if param_name in parameters:
                validated_params[param_name] = parameters[param_name]
            elif is_required:
                raise ValueError(f"Required parameter '{param_name}' is missing")
            elif default_value is not None:
                validated_params[param_name] = default_value
        
        return validated_params
    
    def create_report_from_template(self, template_id: str, data_sources: Dict[str, Any], parameters: Dict = None) -> Dict:
        """Create a report from a template with provided data and parameters"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Validate parameters
        if parameters is None:
            parameters = {}
        validated_params = self.validate_parameters(template_id, parameters)
        
        # Create report structure
        report = {
            "id": f"report_{int(datetime.now().timestamp())}",
            "template_id": template_id,
            "parameters": validated_params,
            "title": template["name"],
            "description": template["description"],
            "created_at": datetime.now().isoformat(),
            "sections": []
        }
        
        # Process each section
        for section in template["sections"]:
            processed_section = section.copy()
            
            # If section has a data source, populate it with actual data
            if "data_source" in section:
                data_source_key = section["data_source"]
                if data_source_key in data_sources:
                    processed_section["data"] = data_sources[data_source_key]
            
            report["sections"].append(processed_section)
        
        return report
    
    def export_report(self, report: Dict, format: str = "json") -> bytes:
        """Export report in specified format"""
        if format.lower() == "json":
            return json.dumps(report, indent=2).encode('utf-8')
        elif format.lower() == "csv":
            # For CSV export, we'll export the first table section
            for section in report.get("sections", []):
                if section.get("type") == "table" and "data" in section:
                    df = pd.DataFrame(section["data"])
                    return df.to_csv(index=False).encode('utf-8')
            # If no table section, export basic report info
            basic_info = {
                "title": report.get("title"),
                "description": report.get("description"),
                "created_at": report.get("created_at")
            }
            df = pd.DataFrame([basic_info])
            return df.to_csv(index=False).encode('utf-8')
        else:
            raise ValueError(f"Unsupported export format: {format}")

# Global instance
report_generator = ReportGenerator()