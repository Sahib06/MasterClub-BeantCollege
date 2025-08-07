#!/usr/bin/env python3
"""
Test script for College Attendance System
This script demonstrates the complete workflow of the attendance system.
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_generate_qr():
    """Test QR code generation"""
    print("📱 Testing QR code generation...")
    
    data = {
        "subject": "Computer Science",
        "class_name": "Computer Science",
        "section": "A",
        "duration_minutes": 10
    }
    
    response = requests.post(f"{BASE_URL}/teacher/generate-qr", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ QR Code generated successfully!")
        print(f"Session Token: {result['session_token']}")
        print(f"Expires At: {result['expires_at']}")
        print(f"QR Code (base64): {result['qr_code'][:50]}...")
        return result
    else:
        print(f"❌ Failed to generate QR code: {response.text}")
        return None

def test_validate_qr(qr_data):
    """Test QR code validation"""
    print("\n🔍 Testing QR code validation...")
    
    data = {
        "qr_data": qr_data
    }
    
    response = requests.post(f"{BASE_URL}/student/validate-qr", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['valid']:
            print("✅ QR code is valid!")
            print(f"Subject: {result['session_info']['subject']}")
            print(f"Class: {result['session_info']['class']}")
            return result['session_info']['session_token']
        else:
            print(f"❌ QR code is invalid: {result['error']}")
            return None
    else:
        print(f"❌ Failed to validate QR code: {response.text}")
        return None

def test_mark_attendance(session_token, student_roll_no):
    """Test attendance marking"""
    print(f"\n📝 Testing attendance marking for {student_roll_no}...")
    
    data = {
        "session_token": session_token,
        "student_roll_no": student_roll_no
    }
    
    response = requests.post(f"{BASE_URL}/student/mark-attendance", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print("✅ Attendance marked successfully!")
            print(f"Student: {result['student_name']}")
            print(f"Timestamp: {result['timestamp']}")
            return True
        else:
            print(f"❌ Failed to mark attendance: {result['error']}")
            return False
    else:
        print(f"❌ Failed to mark attendance: {response.text}")
        return False

def test_get_attendance_history(student_roll_no):
    """Test getting attendance history"""
    print(f"\n📊 Testing attendance history for {student_roll_no}...")
    
    response = requests.get(f"{BASE_URL}/student/attendance-history/{student_roll_no}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Attendance history retrieved!")
        print(f"Student: {result['student_name']}")
        print(f"Roll No: {result['roll_no']}")
        print(f"Class: {result['class']}")
        print(f"Total Records: {result['attendance_count']}")
        
        if result['attendance_records']:
            print("Recent attendance records:")
            for record in result['attendance_records'][:3]:  # Show last 3
                print(f"  - {record['subject']} ({record['teacher']}) at {record['timestamp']}")
        return True
    else:
        print(f"❌ Failed to get attendance history: {response.text}")
        return False

def test_get_teacher_sessions():
    """Test getting teacher sessions"""
    print("\n👨‍🏫 Testing teacher sessions...")
    
    response = requests.get(f"{BASE_URL}/teacher/sessions")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        sessions = response.json()
        print(f"✅ Retrieved {len(sessions)} sessions")
        
        if sessions:
            latest_session = sessions[0]
            print(f"Latest session: {latest_session['subject']} - {latest_session['class_name']}")
            print(f"Attendance count: {latest_session['attendance_count']}")
            return latest_session['id']
        return None
    else:
        print(f"❌ Failed to get teacher sessions: {response.text}")
        return None

def test_get_session_attendance(session_id):
    """Test getting session attendance"""
    print(f"\n📋 Testing session attendance for session {session_id}...")
    
    response = requests.get(f"{BASE_URL}/teacher/sessions/{session_id}/attendance")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Session attendance retrieved!")
        print(f"Subject: {result['session_info']['subject']}")
        print(f"Class: {result['session_info']['class']}")
        print(f"Total Attendance: {result['attendance_count']}")
        
        if result['attendance_records']:
            print("Attendance records:")
            for record in result['attendance_records']:
                print(f"  - {record['student_name']} ({record['roll_no']}) at {record['timestamp']}")
        return True
    else:
        print(f"❌ Failed to get session attendance: {response.text}")
        return False

def main():
    """Run the complete test workflow"""
    print("🚀 College Attendance System - Test Workflow")
    print("=" * 50)
    
    # Test health check
    test_health_check()
    
    # Test QR code generation
    qr_result = test_generate_qr()
    if not qr_result:
        print("❌ Cannot continue without QR code generation")
        return
    
    # Create QR data for validation
    qr_data = json.dumps(qr_result['session_info'])
    
    # Test QR validation
    session_token = test_validate_qr(qr_data)
    if not session_token:
        print("❌ Cannot continue without valid session token")
        return
    
    # Test attendance marking for multiple students
    test_students = ["CS2024001", "CS2024002", "CS2024003"]
    
    for student_roll_no in test_students:
        test_mark_attendance(session_token, student_roll_no)
        time.sleep(1)  # Small delay between requests
    
    # Test attendance history
    test_get_attendance_history("CS2024001")
    
    # Test teacher sessions
    session_id = test_get_teacher_sessions()
    
    # Test session attendance
    if session_id:
        test_get_session_attendance(session_id)
    
    print("\n🎉 Test workflow completed!")
    print("\n📋 Next Steps:")
    print("1. Visit http://localhost:8000/docs for interactive API documentation")
    print("2. Try the endpoints manually using the Swagger UI")
    print("3. Build a frontend application to use these APIs")

if __name__ == "__main__":
    main() 