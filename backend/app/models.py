"""Database models for attendance tracking."""

from sqlalchemy import Column, Integer, String, Date, Time, DateTime, Float
from sqlalchemy.sql import func
from datetime import datetime
from database import Base


class Attendance(Base):
    """Attendance record model."""
    
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(255), index=True, nullable=False)
    class_name = Column(String(255), index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    status = Column(String(20), nullable=False)  # 'present' or 'absent'
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, student='{self.student_name}', date={self.date}, status='{self.status}')>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "student_name": self.student_name,
            "class_name": self.class_name,
            "date": str(self.date),
            "status": self.status,
            "time_in": str(self.time_in) if self.time_in else None,
            "time_out": str(self.time_out) if self.time_out else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AttendancePrediction(Base):
    """AI attendance prediction model."""
    
    __tablename__ = "attendance_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(255), index=True, nullable=False)
    predicted_date = Column(Date, index=True, nullable=False)
    predicted_status = Column(String(20), nullable=False)  # 'likely_present' or 'likely_absent'
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    reason = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<Prediction(student='{self.student_name}', date={self.predicted_date}, status='{self.predicted_status}', confidence={self.confidence})>"


class Anomaly(Base):
    """Anomaly detection records."""
    
    __tablename__ = "anomalies"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(255), index=True, nullable=False)
    anomaly_type = Column(String(50), nullable=False)  # 'unusual_absence', 'pattern_change', etc.
    severity = Column(String(20), nullable=False)  # 'low', 'medium', 'high'
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    resolved = Column(String(20), default="pending")  # 'pending', 'acknowledged', 'resolved'
    
    def __repr__(self):
        return f"<Anomaly(student='{self.student_name}', type='{self.anomaly_type}', severity='{self.severity}')>"
