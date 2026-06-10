"""API routes for attendance management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date as date_type, timedelta
from typing import List, Optional

from database import get_db
from models import Attendance, AttendancePrediction, Anomaly
from schemas import (
    AttendanceCreate, AttendanceUpdate, AttendanceResponse,
    AttendanceStats, PredictionResponse, AnomalyResponse
)

router = APIRouter()


# ============= ATTENDANCE CRUD =============

@router.get("/attendance", response_model=List[AttendanceResponse])
def get_attendance(
    db: Session = Depends(get_db),
    student_name: Optional[str] = Query(None),
    class_name: Optional[str] = Query(None),
    date: Optional[date_type] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """Get attendance records with optional filtering."""
    query = db.query(Attendance)
    
    # Apply filters
    if student_name:
        query = query.filter(Attendance.student_name.ilike(f"%{student_name}%"))
    if class_name:
        query = query.filter(Attendance.class_name.ilike(f"%{class_name}%"))
    if date:
        query = query.filter(Attendance.date == date)
    if status:
        query = query.filter(Attendance.status == status)
    
    # Apply pagination and sorting
    records = query.order_by(Attendance.date.desc()).offset(skip).limit(limit).all()
    
    return records


@router.post("/attendance", response_model=AttendanceResponse, status_code=201)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    """Create a new attendance record."""
    # Validate status
    if attendance.status not in ["present", "absent"]:
        raise HTTPException(
            status_code=400,
            detail="Status must be 'present' or 'absent'"
        )
    
    # Create new record
    db_attendance = Attendance(
        student_name=attendance.student_name,
        class_name=attendance.class_name,
        date=attendance.date,
        status=attendance.status,
        time_in=attendance.time_in,
        time_out=attendance.time_out,
        notes=attendance.notes
    )
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    return db_attendance


@router.get("/attendance/{record_id}", response_model=AttendanceResponse)
def get_attendance_by_id(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific attendance record by ID."""
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Attendance record with ID {record_id} not found"
        )
    
    return record


@router.put("/attendance/{record_id}", response_model=AttendanceResponse)
def update_attendance(
    record_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    """Update an attendance record."""
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Attendance record with ID {record_id} not found"
        )
    
    # Update only provided fields
    update_data = attendance.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(record, field, value)
    
    db.commit()
    db.refresh(record)
    
    return record


@router.delete("/attendance/{record_id}", status_code=204)
def delete_attendance(
    record_id: int,
    db: Session = Depends(get_db)
):
    """Delete an attendance record."""
    record = db.query(Attendance).filter(Attendance.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=404,
            detail=f"Attendance record with ID {record_id} not found"
        )
    
    db.delete(record)
    db.commit()
    
    return None


# ============= STATISTICS =============

@router.get("/attendance/stats", response_model=AttendanceStats)
def get_attendance_stats(
    db: Session = Depends(get_db),
    class_name: Optional[str] = Query(None),
    date: Optional[date_type] = Query(None),
    student_name: Optional[str] = Query(None)
):
    """Get attendance statistics."""
    query = db.query(Attendance)
    
    if class_name:
        query = query.filter(Attendance.class_name == class_name)
    if date:
        query = query.filter(Attendance.date == date)
    if student_name:
        query = query.filter(Attendance.student_name == student_name)
    
    records = query.all()
    
    if not records:
        return AttendanceStats(total=0, present=0, absent=0, attendance_rate=0.0)
    
    total = len(records)
    present = len([r for r in records if r.status == "present"])
    absent = len([r for r in records if r.status == "absent"])
    attendance_rate = (present / total * 100) if total > 0 else 0
    
    return AttendanceStats(
        total=total,
        present=present,
        absent=absent,
        attendance_rate=round(attendance_rate, 2)
    )


# ============= AI/ML ENDPOINTS =============

@router.get("/predict", response_model=List[PredictionResponse])
def get_predictions(
    db: Session = Depends(get_db),
    student_name: Optional[str] = Query(None),
    days_ahead: int = Query(7, ge=1, le=30)
):
    """Get attendance predictions for students."""
    predictions = db.query(AttendancePrediction)
    
    if student_name:
        predictions = predictions.filter(AttendancePrediction.student_name == student_name)
    
    # Filter for future dates
    today = date_type.today()
    future_date = today + timedelta(days=days_ahead)
    predictions = predictions.filter(
        AttendancePrediction.predicted_date.between(today, future_date)
    ).all()
    
    result = []
    for pred in predictions:
        result.append(PredictionResponse(
            student_name=pred.student_name,
            predicted_date=str(pred.predicted_date),
            predicted_status=pred.predicted_status,
            confidence=pred.confidence,
            reason=pred.reason
        ))
    
    return result


@router.get("/anomalies", response_model=List[AnomalyResponse])
def get_anomalies(
    db: Session = Depends(get_db),
    student_name: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    resolved: Optional[str] = Query(None)
):
    """Get detected anomalies in attendance patterns."""
    query = db.query(Anomaly)
    
    if student_name:
        query = query.filter(Anomaly.student_name == student_name)
    if severity:
        query = query.filter(Anomaly.severity == severity)
    if resolved:
        query = query.filter(Anomaly.resolved == resolved)
    
    anomalies = query.order_by(Anomaly.created_at.desc()).all()
    
    return anomalies


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Web Attendance Tracker API",
        "version": "1.0.0"
    }
