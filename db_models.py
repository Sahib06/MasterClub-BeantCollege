from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from college_attendance.database import Base
import uuid
from datetime import datetime, timedelta

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    sessions = relationship("Session", back_populates="teacher")

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_no = Column(String(20), unique=True, nullable=False)
    class_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    father_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationship
    attendances = relationship("Attendance", back_populates="student")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    class_name = Column(String(50), nullable=False)
    section = Column(String(10), nullable=True)
    generated_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    teacher = relationship("Teacher", back_populates="sessions")
    attendances = relationship("Attendance", back_populates="session")
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    timestamp = Column(DateTime, default=func.now())
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    
    # Relationship
    session = relationship("Session", back_populates="attendances")
    student = relationship("Student", back_populates="attendances") 