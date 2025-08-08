#!/usr/bin/env python3
"""
MasterClub-BeantCollege Attendance System
Complete FastAPI application
"""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
import uuid
from datetime import datetime, timedelta
import qrcode
import base64
from io import BytesIO
from passlib.context import CryptContext

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./college_attendance.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database Models
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_no = Column(String(20), unique=True, nullable=False)
    class_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    father_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    class_name = Column(String(50), nullable=False)
    section = Column(String(10), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="MasterClub-BeantCollege Attendance System",
    description="QR code-based attendance system for Beant College",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class GenerateQRRequest(BaseModel):
    subject: str
    class_name: str
    section: str = ""
    duration_minutes: int = 10

class MarkAttendanceRequest(BaseModel):
    session_token: str
    student_roll_no: str
    student_name: Optional[str] = None
    father_name: Optional[str] = None

# Routes
@app.get("/")
async def root():
    return {
        "message": "MasterClub-BeantCollege Attendance System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "frontend": "/ui"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ui")
async def serve_frontend():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    elif os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {"message": "Frontend not found"}

@app.post("/teacher/generate-qr")
async def generate_qr(request: GenerateQRRequest, db: Session = Depends(get_db)):
    # Create session
    expires_at = datetime.utcnow() + timedelta(minutes=request.duration_minutes)
    session = Session(
        teacher_id=1,  # Default teacher
        subject=request.subject,
        class_name=request.class_name,
        section=request.section,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    # Generate QR code
    qr_data = f"session_token:{session.session_token};subject:{session.subject};class:{session.class_name};section:{session.section}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return {
        "qr_code": qr_base64,
        "session_token": session.session_token,
        "expires_at": session.expires_at.isoformat(),
        "session_info": {
            "subject": session.subject,
            "class": session.class_name,
            "section": session.section
        }
    }

@app.post("/student/mark-attendance")
async def mark_attendance(request: MarkAttendanceRequest, db: Session = Depends(get_db), http_request: Request = None):
    # Get session
    session = db.query(Session).filter(Session.session_token == request.session_token).first()
    if not session:
        return {"success": False, "error": "Invalid session token"}
    
    if session.expires_at < datetime.utcnow():
        return {"success": False, "error": "Session has expired"}
    
    # Get student
    student = db.query(Student).filter(Student.roll_no == request.student_roll_no).first()
    if not student:
        return {"success": False, "error": "Student not found"}
    
    # Check if already marked attendance
    existing_attendance = db.query(Attendance).filter(
        Attendance.session_id == session.id,
        Attendance.student_id == student.id
    ).first()
    
    if existing_attendance:
        return {"success": False, "error": "Attendance already marked for this session"}
    
    # Mark attendance
    ip_address = None
    user_agent = None
    if http_request:
        if http_request.headers.get("x-forwarded-for"):
            ip_address = http_request.headers.get("x-forwarded-for").split(",")[0]
        elif http_request.headers.get("x-real-ip"):
            ip_address = http_request.headers.get("x-real-ip")
        else:
            ip_address = http_request.client.host if http_request.client else None
        user_agent = http_request.headers.get("user-agent")
    
    attendance = Attendance(
        session_id=session.id,
        student_id=student.id,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(attendance)
    db.commit()
    
    return {
        "success": True,
        "message": f"Attendance marked successfully for {student.name}",
        "student_name": student.name,
        "timestamp": attendance.timestamp.isoformat()
    }

@app.get("/teacher/sessions")
async def get_sessions(db: Session = Depends(get_db)):
    sessions = db.query(Session).order_by(Session.generated_at.desc()).limit(10).all()
    return [
        {
            "id": session.id,
            "subject": session.subject,
            "class_name": session.class_name,
            "section": session.section,
            "generated_at": session.generated_at.isoformat(),
            "expires_at": session.expires_at.isoformat(),
            "is_active": session.is_active,
            "attendance_count": db.query(Attendance).filter(Attendance.session_id == session.id).count()
        }
        for session in sessions
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port) 
