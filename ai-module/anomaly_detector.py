"""Anomaly detection module for attendance patterns."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import datetime


class AnomalyDetector:
    """Detects anomalies in attendance patterns."""
    
    def __init__(self, threshold=0.7):
        """Initialize the anomaly detector."""
        self.threshold = threshold
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
    
    def extract_features(self, records):
        """Extract features from attendance records."""
        if not records:
            return None
        
        df = pd.DataFrame(records)
        
        # Group by student
        student_stats = {}
        
        for student in df['student_name'].unique():
            student_data = df[df['student_name'] == student]
            
            # Calculate statistics
            total = len(student_data)
            present = len(student_data[student_data['status'] == 'present'])
            absent = total - present
            
            # Calculate rate
            attendance_rate = present / total if total > 0 else 0
            
            # Recent trend (last 5 records)
            recent = student_data.tail(5)
            recent_rate = len(recent[recent['status'] == 'present']) / len(recent) if len(recent) > 0 else 0
            
            student_stats[student] = {
                'total_records': total,
                'present_count': present,
                'absent_count': absent,
                'attendance_rate': attendance_rate,
                'recent_rate': recent_rate,
                'rate_change': attendance_rate - recent_rate
            }
        
        return student_stats
    
    def detect_anomalies(self, records, threshold=None):
        """Detect anomalies in attendance patterns."""
        if threshold:
            self.threshold = threshold
        
        anomalies = []
        stats = self.extract_features(records)
        
        if not stats:
            return anomalies
        
        for student, data in stats.items():
            # Check for sudden changes
            if abs(data['rate_change']) > 0.3:
                severity = 'high' if abs(data['rate_change']) > 0.5 else 'medium'
                anomalies.append({
                    'student_name': student,
                    'anomaly_type': 'pattern_change',
                    'severity': severity,
                    'description': f"Attendance pattern changed significantly. Change: {data['rate_change']:.2%}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check for consistently low attendance
            if data['attendance_rate'] < 0.5 and data['total_records'] >= 10:
                anomalies.append({
                    'student_name': student,
                    'anomaly_type': 'low_attendance',
                    'severity': 'high',
                    'description': f"Low attendance rate: {data['attendance_rate']:.2%}",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check for recent absences
            if data['recent_rate'] < 0.4 and data['total_records'] >= 5:
                anomalies.append({
                    'student_name': student,
                    'anomaly_type': 'recent_absences',
                    'severity': 'medium',
                    'description': f"High absence rate recently: {1 - data['recent_rate']:.2%}",
                    'timestamp': datetime.now().isoformat()
                })
        
        return anomalies
    
    def get_risk_level(self, student_name, records):
        """Get risk level for a specific student."""
        stats = self.extract_features(records)
        
        if student_name not in stats:
            return None
        
        data = stats[student_name]
        
        # Calculate risk score (0-1)
        risk_score = 0
        
        # Lower attendance = higher risk
        if data['attendance_rate'] < 0.7:
            risk_score += (0.7 - data['attendance_rate']) / 0.7
        
        # Negative trend = higher risk
        if data['rate_change'] < 0:
            risk_score += abs(data['rate_change'])
        
        risk_score = min(risk_score / 2, 1.0)  # Normalize to 0-1
        
        # Determine risk level
        if risk_score > 0.7:
            risk_level = 'high'
        elif risk_score > 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'student_name': student_name,
            'risk_level': risk_level,
            'risk_score': float(risk_score),
            'attendance_rate': float(data['attendance_rate']),
            'recent_trend': 'improving' if data['rate_change'] > 0 else 'declining' if data['rate_change'] < 0 else 'stable'
        }
