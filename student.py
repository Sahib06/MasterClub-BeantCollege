from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel

from college_attendance.database import get_db
from college_attendance.services.attendance import AttendanceService
from college_attendance.services.qr_generator import QRGenerator

router = APIRouter(prefix="/student", tags=["student"])

# Pydantic models for request/response
class ValidateQRRequest(BaseModel):
    qr_data: str

class ValidateQRResponse(BaseModel):
    valid: bool
    session_info: Dict[str, Any] = None
    error: str = None

class MarkAttendanceRequest(BaseModel):
    session_token: str
    student_roll_no: str
    student_name: str = None
    father_name: str = None

class MarkAttendanceResponse(BaseModel):
    success: bool
    message: str = None
    error: str = None
    student_name: str = None
    timestamp: str = None

@router.post("/validate-qr", response_model=ValidateQRResponse)
async def validate_qr_code(request: ValidateQRRequest):
    """
    Validate QR code data and return session information
    """
    try:
        # Parse QR data
        session_data = QRGenerator.parse_qr_data(request.qr_data)
        
        # Check if session is expired
        if QRGenerator.is_session_expired(session_data):
            return ValidateQRResponse(
                valid=False,
                error="QR code has expired"
            )
        
        return ValidateQRResponse(
            valid=True,
            session_info=session_data
        )
        
    except ValueError as e:
        return ValidateQRResponse(
            valid=False,
            error=f"Invalid QR code: {str(e)}"
        )
    except Exception as e:
        return ValidateQRResponse(
            valid=False,
            error=f"Error processing QR code: {str(e)}"
        )

@router.post("/mark-attendance", response_model=MarkAttendanceResponse)
async def mark_attendance(
    request: MarkAttendanceRequest,
    db: Session = Depends(get_db),
    http_request: Request = None
):
    """
    Mark attendance for a student with enhanced validation
    """
    try:
        # Get client information
        ip_address = None
        user_agent = None
        
        if http_request:
            # Get IP address
            if http_request.headers.get("x-forwarded-for"):
                ip_address = http_request.headers.get("x-forwarded-for").split(",")[0]
            elif http_request.headers.get("x-real-ip"):
                ip_address = http_request.headers.get("x-real-ip")
            else:
                ip_address = http_request.client.host if http_request.client else None
            
            # Get user agent
            user_agent = http_request.headers.get("user-agent")
        
        # Validate student details if provided
        if request.student_name and request.father_name:
            student = AttendanceService.get_student_by_roll_no(db, request.student_roll_no)
            if not student:
                return MarkAttendanceResponse(
                    success=False,
                    error="Student not found with this roll number"
                )
            
            # Validate student name and father's name
            if student.name.lower() != request.student_name.lower():
                return MarkAttendanceResponse(
                    success=False,
                    error="Student name does not match the roll number"
                )
            
            if student.father_name and student.father_name.lower() != request.father_name.lower():
                return MarkAttendanceResponse(
                    success=False,
                    error="Father's name does not match the student record"
                )
        
        # Mark attendance
        result = AttendanceService.mark_attendance(
            db=db,
            session_token=request.session_token,
            student_roll_no=request.student_roll_no,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        if result.get("success"):
            return MarkAttendanceResponse(
                success=True,
                message=result["message"],
                student_name=result["student_name"],
                timestamp=result["timestamp"]
            )
        else:
            return MarkAttendanceResponse(
                success=False,
                error=result["error"]
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark attendance: {str(e)}")

@router.get("/attendance-history/{student_roll_no}")
async def get_attendance_history(
    student_roll_no: str,
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Get attendance history for a student
    """
    # Get student
    student = AttendanceService.get_student_by_roll_no(db, student_roll_no)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get attendance history
    attendances = AttendanceService.get_student_attendance(db, student.id, limit)
    
    from college_attendance.models.db_models import Session as DBSession
    
    attendance_records = []
    for attendance in attendances:
        session = db.query(DBSession).filter(DBSession.id == attendance.session_id).first()
        attendance_records.append({
            "subject": session.subject,
            "class": session.class_name,
            "section": session.section,
            "teacher": session.teacher.name,
            "timestamp": attendance.timestamp.isoformat(),
            "ip_address": attendance.ip_address,
            "location": attendance.location
        })
    
    return {
        "student_name": student.name,
        "roll_no": student.roll_no,
        "class": student.class_name,
        "attendance_count": len(attendance_records),
        "attendance_records": attendance_records
    }

@router.get("/student-info/{student_roll_no}")
async def get_student_info(
    student_roll_no: str,
    db: Session = Depends(get_db)
):
    """
    Get basic student information
    """
    student = AttendanceService.get_student_by_roll_no(db, student_roll_no)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "name": student.name,
        "roll_no": student.roll_no,
        "class": student.class_name,
        "email": student.email
    } 