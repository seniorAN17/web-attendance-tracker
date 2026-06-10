"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from enum import Enum


class StatusEnum(str, Enum):
    """Attendance status enum."""
    present = "present"
    absent = "absent"


class PredictionStatusEnum(str, Enum):
    """Prediction status enum."""
    likely_present = "likely_present"
    likely_absent = "likely_absent"


class AttendanceCreate(BaseModel):
    """Schema for creating attendance records."""
    student_name: str = Field(..., min_length=1, max_length=255)
    class_name: str = Field(..., min_length=1, max_length=255)
    date: date
    status: StatusEnum
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    notes: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "student_name": "John Doe",
                "class_name": "Python 101",
                "date": "2025-01-15",
                "status": "present",
                "time_in": "09:00:00",
                "time_out": "11:00:00",
                "notes": "On time"
            }
        }


class AttendanceUpdate(BaseModel):
    """Schema for updating attendance records."""
    student_name: Optional[str] = None
    class_name: Optional[str] = None
    date: Optional[date] = None
    status: Optional[StatusEnum] = None
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    notes: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "status": "absent",
                "notes": "Sick leave"
            }
        }


class AttendanceResponse(BaseModel):
    """Schema for attendance response."""
    id: int
    student_name: str
    class_name: str
    date: str
    status: str
    time_in: Optional[str] = None
    time_out: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class AttendanceStats(BaseModel):
    """Schema for attendance statistics."""
    total: int
    present: int
    absent: int
    attendance_rate: float
    
    class Config:
        schema_extra = {
            "example": {
                "total": 30,
                "present": 28,
                "absent": 2,
                "attendance_rate": 93.33
            }
        }


class PredictionResponse(BaseModel):
    """Schema for prediction response."""
    student_name: str
    predicted_date: str
    predicted_status: str
    confidence: float
    reason: Optional[str] = None


class AnomalyResponse(BaseModel):
    """Schema for anomaly detection response."""
    id: int
    student_name: str
    anomaly_type: str
    severity: str
    description: str
    created_at: str
    resolved: str
    
    class Config:
        from_attributes = True
