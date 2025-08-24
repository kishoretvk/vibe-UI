import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from typing import Dict, Any, List, Tuple, Optional
import json

class AnomalyDetector:
    """Anomaly detection module for identifying outliers in datasets"""
    
    def __init__(self):
        """Initialize the anomaly detector"""
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
    
    def detect_anomalies(self, data: List[Dict[str, Any]], method: str = "isolation_forest") -> Dict[str, Any]:
        """
        Detect anomalies in the given data
        
        Args:
            data: List of data records
            method: Anomaly detection method ("isolation_forest", "dbscan", or "statistical")
            
        Returns:
            Dictionary containing anomaly detection results
        """
        if not data:
            return {"anomalies": [], "summary": "No data provided"}
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Select numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_columns:
                return {"anomalies": [], "summary": "No numeric columns found for anomaly detection"}
            
            # Extract numeric data
            numeric_data = df[numeric_columns].fillna(0)
            
            # Detect anomalies based on method
            if method == "isolation_forest":
                results = self._detect_with_isolation_forest(numeric_data, df)
            elif method == "dbscan":
                results = self._detect_with_dbscan(numeric_data, df)
            elif method == "statistical":
                results = self._detect_with_statistical_method(numeric_data, df)
            else:
                results = self._detect_with_isolation_forest(numeric_data, df)
            
            return results
            
        except Exception as e:
            return {
                "anomalies": [],
                "summary": f"Error during anomaly detection: {str(e)}",
                "error": True
            }
    
    def _detect_with_isolation_forest(self, numeric_data: pd.DataFrame, original_data: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies using Isolation Forest algorithm"""
        try:
            # Scale the data
            scaled_data = self.scaler.fit_transform(numeric_data)
            
            # Fit the model
            self.isolation_forest.fit(scaled_data)
            
            # Predict anomalies (-1 for anomaly, 1 for normal)
            predictions = self.isolation_forest.predict(scaled_data)
            anomaly_scores = self.isolation_forest.decision_function(scaled_data)
            
            # Extract anomalies
            anomaly_indices = np.where(predictions == -1)[0]
            anomalies = []
            
            for idx in anomaly_indices:
                anomaly_record = original_data.iloc[idx].to_dict()
                anomaly_record["anomaly_score"] = float(anomaly_scores[idx])
                anomaly_record["index"] = int(idx)
                anomalies.append(anomaly_record)
            
            return {
                "anomalies": anomalies,
                "summary": f"Detected {len(anomalies)} anomalies using Isolation Forest",
                "method": "isolation_forest",
                "total_records": len(original_data),
                "anomaly_count": len(anomalies)
            }
            
        except Exception as e:
            return {
                "anomalies": [],
                "summary": f"Error in Isolation Forest detection: {str(e)}",
                "method": "isolation_forest",
                "error": True
            }
    
    def _detect_with_dbscan(self, numeric_data: pd.DataFrame, original_data: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies using DBSCAN clustering algorithm"""
        try:
            # Scale the data
            scaled_data = self.scaler.fit_transform(numeric_data)
            
            # Fit DBSCAN
            cluster_labels = self.dbscan.fit_predict(scaled_data)
            
            # Points labeled as -1 are considered noise/anomalies
            anomaly_indices = np.where(cluster_labels == -1)[0]
            anomalies = []
            
            for idx in anomaly_indices:
                anomaly_record = original_data.iloc[idx].to_dict()
                anomaly_record["cluster_label"] = int(cluster_labels[idx])
                anomaly_record["index"] = int(idx)
                anomalies.append(anomaly_record)
            
            return {
                "anomalies": anomalies,
                "summary": f"Detected {len(anomalies)} anomalies using DBSCAN",
                "method": "dbscan",
                "total_records": len(original_data),
                "anomaly_count": len(anomalies)
            }
            
        except Exception as e:
            return {
                "anomalies": [],
                "summary": f"Error in DBSCAN detection: {str(e)}",
                "method": "dbscan",
                "error": True
            }
    
    def _detect_with_statistical_method(self, numeric_data: pd.DataFrame, original_data: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies using statistical methods (z-score)"""
        try:
            anomalies = []
            
            # For each numeric column, calculate z-scores and identify outliers
            for column in numeric_data.columns:
                series = numeric_data[column]
                mean = series.mean()
                std = series.std()
                
                if std == 0:  # Skip columns with no variance
                    continue
                
                z_scores = np.abs((series - mean) / std)
                outlier_indices = np.where(z_scores > 3)[0]  # Z-score > 3 is considered an outlier
                
                for idx in outlier_indices:
                    # Check if this record is already identified as anomaly
                    existing_anomaly = next((a for a in anomalies if a.get("index") == int(idx)), None)
                    if not existing_anomaly:
                        anomaly_record = original_data.iloc[idx].to_dict()
                        anomaly_record["index"] = int(idx)
                        anomaly_record["outlier_columns"] = [column]
                        anomaly_record["z_score"] = float(z_scores[idx])
                        anomalies.append(anomaly_record)
                    else:
                        # Add this column to the existing anomaly record
                        if "outlier_columns" in existing_anomaly:
                            existing_anomaly["outlier_columns"].append(column)
                        else:
                            existing_anomaly["outlier_columns"] = [column]
            
            return {
                "anomalies": anomalies,
                "summary": f"Detected {len(anomalies)} anomalies using statistical methods (z-score > 3)",
                "method": "statistical",
                "total_records": len(original_data),
                "anomaly_count": len(anomalies)
            }
            
        except Exception as e:
            return {
                "anomalies": [],
                "summary": f"Error in statistical detection: {str(e)}",
                "method": "statistical",
                "error": True
            }
    
    def get_detection_methods(self) -> List[str]:
        """Get available detection methods"""
        return ["isolation_forest", "dbscan", "statistical"]