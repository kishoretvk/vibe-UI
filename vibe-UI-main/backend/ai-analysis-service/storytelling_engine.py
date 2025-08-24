import requests
import json
import os
from typing import Dict, Any, List, Optional

class StorytellingEngine:
    """AI-powered storytelling engine that generates insights from data"""
    
    def __init__(self):
        """Initialize the storytelling engine"""
        self.llm_service_url = os.getenv('LLM_SERVICE_URL', 'http://llm-integration-service:5005')
        self.anomaly_service_url = os.getenv('ANOMALY_SERVICE_URL', 'http://anomaly-detection-service:5006')
    
    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze data and generate storytelling insights
        
        Args:
            data: List of data records
            
        Returns:
            Dictionary containing storytelling insights
        """
        try:
            # Detect anomalies in the data
            anomalies = self._detect_anomalies(data)
            
            # Prepare data description
            data_description = self._describe_data(data)
            data_sample = self._create_sample(data)
            
            # Call LLM integration service
            llm_response = self._call_llm_service(data_description, data_sample)
            
            if llm_response:
                # Add anomaly information to the insights
                if anomalies and anomalies.get("anomalies"):
                    anomaly_insight = {
                        "type": "anomaly",
                        "description": f"Detected {anomalies['anomaly_count']} anomalies in the data using {anomalies['method']} method.",
                        "confidence": 0.95,
                        "details": anomalies.get("anomalies", [])[:3]  # Limit to first 3 anomalies
                    }
                    llm_response["insights"].append(anomaly_insight)
                return llm_response
            
            # Fallback if LLM service fails
            return self._create_fallback_insights()
            
        except Exception as e:
            # Fallback if there's an error
            return self._create_fallback_insights()
    
    def _describe_data(self, data: List[Dict[str, Any]]) -> str:
        """
        Create a description of the data structure
        
        Args:
            data: List of data records
            
        Returns:
            String description of the data
        """
        if not data:
            return "Empty dataset"
        
        # Get column names
        columns = list(data[0].keys()) if data else []
        
        # Get data types
        types = {}
        for col in columns:
            if data and col in data[0]:
                types[col] = type(data[0][col]).__name__
        
        return f"Dataset with {len(data)} records and columns: {', '.join(columns)} (types: {', '.join([f'{k}:{v}' for k,v in types.items()])})"
    
    def _create_sample(self, data: List[Dict[str, Any]], max_records: int = 5) -> str:
        """
        Create a sample of the data for context
        
        Args:
            data: List of data records
            max_records: Maximum number of records to include in sample
            
        Returns:
            JSON string of sample data
        """
        if not data:
            return ""
        
        sample = data[:max_records]
        return json.dumps(sample, indent=2)
    
    def _call_llm_service(self, data_description: str, data_sample: str) -> Optional[Dict[str, Any]]:
        """
        Call the LLM integration service to generate insights
        
        Args:
            data_description: Description of the data
            data_sample: Sample of the data
            
        Returns:
            Dictionary with insights or None if failed
        """
        try:
            response = requests.post(
                f"{self.llm_service_url}/api/storytelling",
                json={
                    "data_description": data_description,
                    "data_sample": data_sample
                },
                timeout=30
            )
            
            if response.status_code == 200:
                llm_data = response.json()
                # Try to parse the insights as JSON, fallback to raw text
                try:
                    insights = json.loads(llm_data.get('insights', '{}'))
                except:
                    insights = {"raw_response": llm_data.get('insights', '')}
                
                return {
                    "title": "AI-Powered Data Insights",
                    "summary": insights.get("summary", "Automated analysis of your data"),
                    "insights": insights.get("insights", []),
                    "recommendations": insights.get("recommendations", [])
                }
            
            return None
            
        except Exception as e:
            print(f"Error calling LLM service: {e}")
            return None
    
    def _detect_anomalies(self, data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Detect anomalies in the data using the anomaly detection service
        
        Args:
            data: List of data records
            
        Returns:
            Dictionary with anomaly detection results or None if failed
        """
        try:
            response = requests.post(
                f"{self.anomaly_service_url}/api/quick-detect",
                json={"data": data},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
        except Exception as e:
            print(f"Error calling anomaly detection service: {e}")
            return None
    
    def _create_fallback_insights(self) -> Dict[str, Any]:
        """
        Create fallback insights when LLM service is unavailable
        
        Returns:
            Dictionary with fallback insights
        """
        return {
            "title": "Data Insights Report",
            "summary": "Analysis of your data trends and patterns.",
            "insights": [
                {
                    "type": "info",
                    "description": "AI analysis service is available.",
                    "confidence": 0.8
                }
            ],
            "recommendations": [
                "Ensure LLM integration service is running for full AI capabilities"
            ]
        }
    
    def generate_chart_insights(self, data_description: str, chart_type: str) -> Dict[str, Any]:
        """
        Generate insights for visualizing data in a specific chart type
        
        Args:
            data_description: Description of the data
            chart_type: Type of chart to visualize the data in
            
        Returns:
            Dictionary with chart visualization insights
        """
        try:
            response = requests.post(
                f"{self.llm_service_url}/api/chart-description",
                json={
                    "data_description": data_description,
                    "chart_type": chart_type
                },
                timeout=30
            )
            
            if response.status_code == 200:
                llm_data = response.json()
                return {
                    "chart_type": chart_type,
                    "description": llm_data.get('description', ''),
                    "model_info": llm_data.get('model_info', {})
                }
            
            return {
                "chart_type": chart_type,
                "description": f"Recommended visualization for {chart_type} chart type.",
                "model_info": {}
            }
            
        except Exception as e:
            print(f"Error calling LLM service for chart insights: {e}")
            return {
                "chart_type": chart_type,
                "description": f"Recommended visualization for {chart_type} chart type.",
                "model_info": {}
            }