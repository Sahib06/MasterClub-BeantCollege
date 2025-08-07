# College Attendance System

A modern QR code-based attendance system for colleges and universities. This system allows teachers to generate unique QR codes for attendance sessions and students to mark their attendance by scanning the QR codes.

## 🚀 Features

### Teacher Features
- Generate unique QR codes for attendance sessions
- Set session duration (default: 10 minutes)
- View session history and attendance records
- Deactivate sessions when needed
- Real-time attendance tracking

### Student Features
- Scan QR codes to validate session information
- Mark attendance with student roll number
- View attendance history
- Automatic IP and device tracking for security

### Security Features
- Session tokens with expiration
- One attendance per session per student
- IP address and user agent logging
- Class validation (students can only mark attendance for their enrolled classes)

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **QR Code**: qrcode library
- **Authentication**: JWT (planned)
- **Password Hashing**: bcrypt

## 📁 Project Structure

```
college_attendance/
├── app/
│   ├── routes/
│   │   ├── teacher.py      # Teacher API endpoints
│   │   └── student.py      # Student API endpoints
│   ├── services/
│   │   ├── qr_generator.py # QR code generation service
│   │   └── attendance.py   # Attendance management service
│   ├── models/
│   │   └── db_models.py    # Database models
│   ├── database.py         # Database configuration
│   └── main.py            # FastAPI application
├── requirements.txt        # Python dependencies
├── seed_data.py          # Database seeding script
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

The system uses SQLite by default for development. The database will be created automatically when you run the application.

### 3. Seed Sample Data

```bash
python seed_data.py
```

This will create sample teachers and students for testing.

### 4. Run the Application

```bash
python -m college_attendance.main
```

Or using uvicorn directly:

```bash
uvicorn college_attendance.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📋 API Endpoints

### Teacher Endpoints

#### Generate QR Code
```http
POST /teacher/generate-qr
Content-Type: application/json

{
  "subject": "Computer Science",
  "class_name": "Computer Science",
  "section": "A",
  "duration_minutes": 10
}
```

#### Get Teacher Sessions
```http
GET /teacher/sessions?limit=20
```

#### Get Session Attendance
```http
GET /teacher/sessions/{session_id}/attendance
```

#### Deactivate Session
```http
DELETE /teacher/sessions/{session_id}
```

### Student Endpoints

#### Validate QR Code
```http
POST /student/validate-qr
Content-Type: application/json

{
  "qr_data": "{\"session_token\":\"...\",\"subject\":\"...\"}"
}
```

#### Mark Attendance
```http
POST /student/mark-attendance
Content-Type: application/json

{
  "session_token": "uuid-session-token",
  "student_roll_no": "CS2024001"
}
```

#### Get Attendance History
```http
GET /student/attendance-history/{student_roll_no}?limit=50
```

#### Get Student Info
```http
GET /student/student-info/{student_roll_no}
```

## 🗄️ Database Schema

### Teachers Table
- `id`: Primary key
- `name`: Teacher name
- `email`: Unique email
- `password_hash`: Hashed password
- `created_at`: Timestamp

### Students Table
- `id`: Primary key
- `name`: Student name
- `roll_no`: Unique roll number
- `class_name`: Student's class
- `email`: Student email
- `created_at`: Timestamp

### Sessions Table
- `id`: Primary key
- `session_token`: Unique session token
- `teacher_id`: Foreign key to teachers
- `subject`: Subject name
- `class_name`: Class name
- `section`: Section (optional)
- `generated_at`: Session creation time
- `expires_at`: Session expiration time
- `is_active`: Session status

### Attendance Table
- `id`: Primary key
- `session_id`: Foreign key to sessions
- `student_id`: Foreign key to students
- `timestamp`: Attendance time
- `ip_address`: Client IP
- `user_agent`: Client user agent
- `location`: Location (optional)

## 🔐 Security Features

1. **Session Expiration**: QR codes expire after a configurable time (default: 10 minutes)
2. **Unique Session Tokens**: Each session has a unique UUID token
3. **One Attendance Per Session**: Students can only mark attendance once per session
4. **Class Validation**: Students can only mark attendance for their enrolled classes
5. **IP Tracking**: Client IP addresses are logged for audit purposes
6. **Device Tracking**: User agent strings are logged for security

## 🧪 Testing

### Sample Data

After running `seed_data.py`, you'll have:

**Teachers:**
- Dr. Sarah Johnson (sarah.johnson@college.edu)
- Prof. Michael Chen (michael.chen@college.edu)
- Dr. Emily Rodriguez (emily.rodriguez@college.edu)

**Students:**
- Computer Science: CS2024001-CS2024005, CS2023001-CS2023003
- Mathematics: MATH2024001-MATH2024003
- Physics: PHY2024001-PHY2024004
- Engineering: ENG2024001-ENG2024005

### Testing Workflow

1. **Generate QR Code**: Use the teacher endpoint to generate a QR code
2. **Validate QR**: Use the student endpoint to validate the QR data
3. **Mark Attendance**: Use the student endpoint to mark attendance
4. **View Records**: Use teacher endpoints to view attendance records

## 🔧 Configuration

### Environment Variables

Create a `.env` file for production settings:

```env
DATABASE_URL=postgresql://user:password@localhost/attendance_db
SECRET_KEY=your-secret-key-here
```

### Database Configuration

- **Development**: SQLite (default)
- **Production**: PostgreSQL (recommended)

## 🚀 Deployment

### Development
```bash
uvicorn college_attendance.main:app --reload
```

### Production
```bash
uvicorn college_attendance.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🔮 Future Enhancements

1. **Authentication**: JWT-based authentication for teachers
2. **Real-time Updates**: WebSocket support for live attendance updates
3. **Mobile App**: React Native mobile application
4. **Analytics**: Attendance analytics and reports
5. **Notifications**: Email/SMS notifications for absent students
6. **Geolocation**: GPS-based attendance validation
7. **Face Recognition**: Biometric attendance marking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please open an issue on GitHub. 