"""Attendance prediction module using machine learning."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta
import joblib
import os


class AttendancePredictor:
    """Predicts future attendance based on historical data."""
    
    def __init__(self, model_path='./ai-module/models/predictor.pkl'):
        """Initialize the predictor."""
        self.model_path = model_path
        self.model = None
        self.label_encoder = None
        self.is_trained = False
        
        # Load model if exists
        if os.path.exists(model_path):
            self.load_model()
    
    def prepare_data(self, records):
        """Prepare data for training or prediction."""
        if not records:
            return None
        
        df = pd.DataFrame(records)
        
        # Convert date to features
        df['date'] = pd.to_datetime(df['date'])
        df['day_of_week'] = df['date'].dt.dayofweek
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        
        return df
    
    def train(self, records):
        """Train the prediction model."""
        df = self.prepare_data(records)
        
        if df is None or len(df) < 10:
            print("Not enough data to train model")
            return False
        
        try:
            # Encode status
            self.label_encoder = LabelEncoder()
            y = self.label_encoder.fit_transform(df['status'])
            
            # Select features
            X = df[['day_of_week', 'month', 'day']].values
            
            # Train model
            self.model = RandomForestClassifier(n_estimators=10, random_state=42)
            self.model.fit(X, y)
            self.is_trained = True
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            
            print(f"✅ Model trained and saved to {self.model_path}")
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            return False
    
    def predict(self, student_name, date):
        """Predict attendance for a student on a given date."""
        if not self.is_trained or self.model is None:
            return None
        
        try:
            # Convert date to features
            dt = pd.to_datetime(date)
            day_of_week = dt.dayofweek
            month = dt.month
            day = dt.day
            
            X = np.array([[day_of_week, month, day]])
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            
            # Get confidence
            confidence = max(probability)
            
            # Decode prediction
            status = self.label_encoder.inverse_transform([prediction])[0]
            
            return {
                "status": status,
                "confidence": float(confidence),
                "reason": f"Based on pattern for {dt.strftime('%A')} in {dt.strftime('%B')}"
            }
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None
    
    def predict_batch(self, student_name, days_ahead=7):
        """Predict attendance for next N days."""
        predictions = []
        
        for i in range(1, days_ahead + 1):
            future_date = datetime.now() + timedelta(days=i)
            pred = self.predict(student_name, future_date)
            
            if pred:
                predictions.append({
                    "student_name": student_name,
                    "predicted_date": future_date.strftime('%Y-%m-%d'),
                    "predicted_status": f"likely_{pred['status']}",
                    "confidence": pred["confidence"],
                    "reason": pred["reason"]
                })
        
        return predictions
    
    def load_model(self):
        """Load a trained model."""
        try:
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            print(f"✅ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def save_model(self):
        """Save the trained model."""
        if self.model:
            joblib.dump(self.model, self.model_path)
