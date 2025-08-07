from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from college_attendance.models.db_models import Session as DBSession, Attendance, Student
from college_attendance.services.qr_generator import QRGenerator

class AttendanceService:
    @staticmethod
    def create_session(
        db: Session,
        teacher_id: int,
        subject: str,
        class_name: str,
        section: str = None,
        duration_minutes: int = 10
    ) -> DBSession:
        """Create a new attendance session"""
        session_token = QRGenerator.generate_session_token()
        expires_at = datetime.utcnow() + timedelta(minutes=duration_minutes)
        
        session = DBSession(
            session_token=session_token,
            teacher_id=teacher_id,
            subject=subject,
            class_name=class_name,
            section=section,
            expires_at=expires_at
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return session
    
    @staticmethod
    def get_session_by_token(db: Session, session_token: str) -> Optional[DBSession]:
        """Get session by token"""
        return db.query(DBSession).filter(
            DBSession.session_token == session_token,
            DBSession.is_active == True
        ).first()
    
    @staticmethod
    def validate_session(db: Session, session_token: str) -> Dict[str, Any]:
        """Validate session token and return session info"""
        session = AttendanceService.get_session_by_token(db, session_token)
        
        if not session:
            return {"valid": False, "error": "Invalid session token"}
        
        if session.is_expired():
            return {"valid": False, "error": "Session has expired"}
        
        return {
            "valid": True,
            "session": session,
            "session_info": {
                "subject": session.subject,
                "class": session.class_name,
                "section": session.section,
                "teacher": session.teacher.name,
                "expires_at": session.expires_at.isoformat()
            }
        }
    
    @staticmethod
    def get_student_by_roll_no(db: Session, roll_no: str) -> Optional[Student]:
        """Get student by roll number"""
        return db.query(Student).filter(Student.roll_no == roll_no).first()
    
    @staticmethod
    def mark_attendance(
        db: Session,
        session_token: str,
        student_roll_no: str,
        ip_address: str = None,
        user_agent: str = None,
        location: str = None
    ) -> Dict[str, Any]:
        """Mark attendance for a student"""
        # Validate session
        session_validation = AttendanceService.validate_session(db, session_token)
        if not session_validation["valid"]:
            return session_validation
        
        session = session_validation["session"]
        
        # Get student
        student = AttendanceService.get_student_by_roll_no(db, student_roll_no)
        if not student:
            return {"success": False, "error": "Student not found"}
        
        # Check if student is in the correct class
        if student.class_name != session.class_name:
            return {"success": False, "error": "Student not enrolled in this class"}
        
        # Check if attendance already marked
        existing_attendance = db.query(Attendance).filter(
            and_(
                Attendance.session_id == session.id,
                Attendance.student_id == student.id
            )
        ).first()
        
        if existing_attendance:
            return {"success": False, "error": "Attendance already marked for this session"}
        
        # Mark attendance
        attendance = Attendance(
            session_id=session.id,
            student_id=student.id,
            ip_address=ip_address,
            user_agent=user_agent,
            location=location
        )
        
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        
        return {
            "success": True,
            "message": "Attendance marked successfully",
            "student_name": student.name,
            "timestamp": attendance.timestamp.isoformat()
        }
    
    @staticmethod
    def get_session_attendance(db: Session, session_id: int) -> list:
        """Get all attendance records for a session"""
        return db.query(Attendance).filter(Attendance.session_id == session_id).all()
    
    @staticmethod
    def get_student_attendance(db: Session, student_id: int, limit: int = 50) -> list:
        """Get attendance history for a student"""
        return db.query(Attendance).filter(
            Attendance.student_id == student_id
        ).order_by(Attendance.timestamp.desc()).limit(limit).all() 