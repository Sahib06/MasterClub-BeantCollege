#!/usr/bin/env python3
"""
Data seeding script for College Attendance System
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from college_attendance.database import SessionLocal, engine
from college_attendance.models.db_models import Base, Teacher, Student
from passlib.context import CryptContext

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def seed_data():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_teachers = db.query(Teacher).count()
        existing_students = db.query(Student).count()
        
        if existing_teachers > 0 or existing_students > 0:
            print("Database already contains data. Skipping seeding.")
            return
        
        # Create sample teachers
        teachers = [
            Teacher(
                name="Dr. Sarah Johnson",
                email="sarah.johnson@college.edu",
                password_hash=hash_password("teacher123")
            ),
            Teacher(
                name="Prof. Michael Chen",
                email="michael.chen@college.edu",
                password_hash=hash_password("teacher123")
            ),
            Teacher(
                name="Dr. Emily Rodriguez",
                email="emily.rodriguez@college.edu",
                password_hash=hash_password("teacher123")
            )
        ]
        
        for teacher in teachers:
            db.add(teacher)
        
        # Create sample students
        students = [
            # Computer Science - Year 1
            Student(name="Alice Johnson", roll_no="CS2024001", class_name="Computer Science", email="alice.johnson@student.edu", father_name="Robert Johnson"),
            Student(name="Bob Smith", roll_no="CS2024002", class_name="Computer Science", email="bob.smith@student.edu", father_name="John Smith"),
            Student(name="Charlie Brown", roll_no="CS2024003", class_name="Computer Science", email="charlie.brown@student.edu", father_name="David Brown"),
            Student(name="Diana Prince", roll_no="CS2024004", class_name="Computer Science", email="diana.prince@student.edu", father_name="Michael Prince"),
            Student(name="Edward Wilson", roll_no="CS2024005", class_name="Computer Science", email="edward.wilson@student.edu", father_name="Thomas Wilson"),
            
            # Computer Science - Year 2
            Student(name="Fiona Garcia", roll_no="CS2023001", class_name="Computer Science", email="fiona.garcia@student.edu", father_name="Carlos Garcia"),
            Student(name="George Lee", roll_no="CS2023002", class_name="Computer Science", email="george.lee@student.edu", father_name="William Lee"),
            Student(name="Hannah Kim", roll_no="CS2023003", class_name="Computer Science", email="hannah.kim@student.edu", father_name="Jin Kim"),
            
            # Mathematics - Year 1
            Student(name="Ian Thompson", roll_no="MATH2024001", class_name="Mathematics", email="ian.thompson@student.edu", father_name="Peter Thompson"),
            Student(name="Julia Davis", roll_no="MATH2024002", class_name="Mathematics", email="julia.davis@student.edu", father_name="Richard Davis"),
            Student(name="Kevin Martinez", roll_no="MATH2024003", class_name="Mathematics", email="kevin.martinez@student.edu", father_name="Jose Martinez"),
            
            # Physics - Year 1
            Student(name="Lisa Anderson", roll_no="PHY2024001", class_name="Physics", email="lisa.anderson@student.edu", father_name="James Anderson"),
            Student(name="Mark Taylor", roll_no="PHY2024002", class_name="Physics", email="mark.taylor@student.edu", father_name="Andrew Taylor"),
            Student(name="Nina Patel", roll_no="PHY2024003", class_name="Physics", email="nina.patel@student.edu", father_name="Raj Patel"),
            Student(name="Oliver White", roll_no="PHY2024004", class_name="Physics", email="oliver.white@student.edu", father_name="Daniel White"),
            
            # Engineering - Year 1
            Student(name="Paula Rodriguez", roll_no="ENG2024001", class_name="Engineering", email="paula.rodriguez@student.edu", father_name="Miguel Rodriguez"),
            Student(name="Quinn Johnson", roll_no="ENG2024002", class_name="Engineering", email="quinn.johnson@student.edu", father_name="Steven Johnson"),
            Student(name="Rachel Green", roll_no="ENG2024003", class_name="Engineering", email="rachel.green@student.edu", father_name="Christopher Green"),
            Student(name="Samuel Black", roll_no="ENG2024004", class_name="Engineering", email="samuel.black@student.edu", father_name="Matthew Black"),
            Student(name="Tina Wong", roll_no="ENG2024005", class_name="Engineering", email="tina.wong@student.edu", father_name="Henry Wong")
        ]
        
        for student in students:
            db.add(student)
        
        # Commit all changes
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(teachers)} teachers")
        print(f"Created {len(students)} students")
        print("\nSample Login Credentials:")
        print("Teacher Email: sarah.johnson@college.edu")
        print("Teacher Password: teacher123")
        print("\nSample Student Roll Numbers:")
        print("CS2024001, CS2024002, MATH2024001, PHY2024001, ENG2024001")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data() 