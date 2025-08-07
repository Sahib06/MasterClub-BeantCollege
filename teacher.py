from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
from datetime import datetime

from college_attendance.database import get_db
from college_attendance.services.qr_generator import QRGenerator
from college_attendance.services.attendance import AttendanceService
from college_attendance.models.db_models import Teacher

router = APIRouter(prefix="/teacher", tags=["teacher"])

# Pydantic models for request/response
class GenerateQRRequest(BaseModel):
    subject: str
    class_name: str
    section: str = None
    duration_minutes: int = 10

class GenerateQRResponse(BaseModel):
    qr_code: str
    session_token: str
    session_info: Dict[str, Any]
    expires_at: str

class SessionInfoResponse(BaseModel):
    id: int
    session_token: str
    subject: str
    class_name: str
    section: str
    generated_at: str
    expires_at: str
    is_active: bool
    attendance_count: int

@router.post("/generate-qr", response_model=GenerateQRResponse)
async def generate_qr_code(
    request: GenerateQRRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    Generate a QR code for attendance session
    """
    # TODO: Add teacher authentication
    # For now, using a default teacher ID
    teacher_id = 1  # This should come from authentication
    
    try:
        # Create session in database
        session = AttendanceService.create_session(
            db=db,
            teacher_id=teacher_id,
            subject=request.subject,
            class_name=request.class_name,
            section=request.section,
            duration_minutes=request.duration_minutes
        )
        
        # Create session data for QR code
        session_data = QRGenerator.create_session_data(
            session_token=session.session_token,
            subject=session.subject,
            class_name=session.class_name,
            section=session.section,
            duration_minutes=request.duration_minutes
        )
        
        # Generate QR code
        qr_code = QRGenerator.generate_qr_code(session_data)
        
        return GenerateQRResponse(
            qr_code=qr_code,
            session_token=session.session_token,
            session_info=session_data,
            expires_at=session.expires_at.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate QR code: {str(e)}")

@router.get("/sessions", response_model=list[SessionInfoResponse])
async def get_teacher_sessions(
    db: Session = Depends(get_db),
    limit: int = 20
):
    """
    Get all sessions for the teacher
    """
    # TODO: Add teacher authentication
    teacher_id = 1  # This should come from authentication
    
    from college_attendance.models.db_models import Session as DBSession, Attendance
    
    sessions = db.query(DBSession).filter(
        DBSession.teacher_id == teacher_id
    ).order_by(DBSession.generated_at.desc()).limit(limit).all()
    
    session_responses = []
    for session in sessions:
        attendance_count = db.query(Attendance).filter(
            Attendance.session_id == session.id
        ).count()
        
        session_responses.append(SessionInfoResponse(
            id=session.id,
            session_token=session.session_token,
            subject=session.subject,
            class_name=session.class_name,
            section=session.section,
            generated_at=session.generated_at.isoformat(),
            expires_at=session.expires_at.isoformat(),
            is_active=session.is_active,
            attendance_count=attendance_count
        ))
    
    return session_responses

@router.get("/sessions/{session_id}/attendance")
async def get_session_attendance(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Get attendance records for a specific session
    """
    # TODO: Add teacher authentication and verify teacher owns this session
    
    from college_attendance.models.db_models import Session as DBSession, Attendance, Student
    
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    attendances = db.query(Attendance).filter(Attendance.session_id == session_id).all()
    
    attendance_records = []
    for attendance in attendances:
        student = db.query(Student).filter(Student.id == attendance.student_id).first()
        attendance_records.append({
            "student_name": student.name,
            "roll_no": student.roll_no,
            "timestamp": attendance.timestamp.isoformat(),
            "ip_address": attendance.ip_address,
            "location": attendance.location
        })
    
    return {
        "session_info": {
            "subject": session.subject,
            "class": session.class_name,
            "section": session.section,
            "generated_at": session.generated_at.isoformat(),
            "expires_at": session.expires_at.isoformat()
        },
        "attendance_count": len(attendance_records),
        "attendance_records": attendance_records
    }

@router.delete("/sessions/{session_id}")
async def deactivate_session(
    session_id: int,
    db: Session = Depends(get_db)
):
    """
    Deactivate a session (mark as inactive)
    """
    # TODO: Add teacher authentication and verify teacher owns this session
    
    from college_attendance.models.db_models import Session as DBSession
    
    session = db.query(DBSession).filter(DBSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.is_active = False
    db.commit()
    
    return {"message": "Session deactivated successfully"} 