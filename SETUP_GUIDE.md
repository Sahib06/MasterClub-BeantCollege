# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

## 🎯 One-Command Setup

Run the startup script to automatically set up everything:

```bash
python run.py
```

This will:
1. ✅ Install all dependencies
2. ✅ Create the database with sample data
3. ✅ Start the server

## 📱 Access the Application

Once the server is running, you can access:

- **🌐 Frontend Interface**: http://localhost:8000/ui
- **📚 API Documentation**: http://localhost:8000/docs
- **🔍 Health Check**: http://localhost:8000/health

## 🧪 Test the System

### Teacher Workflow:
1. Go to http://localhost:8000/ui
2. Click "Teacher Dashboard"
3. Fill in the form and generate a QR code
4. Display the QR code to students

### Student Workflow:
1. Go to http://localhost:8000/ui
2. Click "Student Portal"
3. Scan the QR code (or paste the data)
4. Enter your roll number (e.g., CS2024001)
5. Mark attendance

## 📋 Sample Data

### Teachers:
- Dr. Sarah Johnson (sarah.johnson@college.edu)
- Prof. Michael Chen (michael.chen@college.edu)
- Dr. Emily Rodriguez (emily.rodriguez@college.edu)

### Students:
- **Computer Science**: CS2024001, CS2024002, CS2024003, CS2024004, CS2024005
- **Mathematics**: MATH2024001, MATH2024002, MATH2024003
- **Physics**: PHY2024001, PHY2024002, PHY2024003, PHY2024004
- **Engineering**: ENG2024001, ENG2024002, ENG2024003, ENG2024004, ENG2024005

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database
python seed_data.py

# 3. Start the server
python -m college_attendance.main
```

## 🧪 Testing with Script

Run the automated test script:

```bash
python test_system.py
```

This will test all the major functionality of the system.

## 📁 Project Structure

```
college_attendance/
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models/
│   └── db_models.py     # Database models
├── routes/
│   ├── teacher.py       # Teacher API endpoints
│   └── student.py       # Student API endpoints
├── services/
│   ├── qr_generator.py  # QR code generation
│   └── attendance.py    # Attendance management
├── requirements.txt      # Python dependencies
├── seed_data.py         # Database seeding
├── test_system.py       # Test script
├── run.py              # Startup script
└── static/
    └── index.html       # Frontend interface
```

## 🔐 Security Features

- ✅ Session tokens with expiration (10 minutes default)
- ✅ One attendance per session per student
- ✅ IP address and device tracking
- ✅ Class validation (students can only mark attendance for their enrolled classes)
- ✅ Unique session tokens (UUID)

## 🚀 API Endpoints

### Teacher Endpoints:
- `POST /teacher/generate-qr` - Generate QR code
- `GET /teacher/sessions` - Get teacher sessions
- `GET /teacher/sessions/{id}/attendance` - Get session attendance
- `DELETE /teacher/sessions/{id}` - Deactivate session

### Student Endpoints:
- `POST /student/validate-qr` - Validate QR code
- `POST /student/mark-attendance` - Mark attendance
- `GET /student/attendance-history/{roll_no}` - Get attendance history
- `GET /student/student-info/{roll_no}` - Get student info

## 🛠️ Troubleshooting

### Common Issues:

1. **Port 8000 already in use**
   ```bash
   # Use a different port
   uvicorn college_attendance.main:app --port 8001
   ```

2. **Database errors**
   ```bash
   # Delete the database file and restart
   rm college_attendance.db
   python seed_data.py
   ```

3. **Import errors**
   ```bash
   # Make sure you're in the project root directory
   # and all dependencies are installed
   pip install -r requirements.txt
   ```

## 📞 Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure you're running from the project root directory
4. Check that port 8000 is available

## 🎉 Success!

Once everything is running, you should see:
- ✅ Server started on http://localhost:8000
- ✅ Database seeded with sample data
- ✅ Frontend accessible at http://localhost:8000/ui
- ✅ API documentation at http://localhost:8000/docs

Happy attendance tracking! 🎓 