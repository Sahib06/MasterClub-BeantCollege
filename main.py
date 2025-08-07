from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from college_attendance.database import engine
from college_attendance.models import db_models
from college_attendance.routes import teacher, student
import os

# Create database tables
db_models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="College Attendance System",
    description="A QR code-based attendance system for colleges",
    version="1.0.0"
)

# Add CORS middleware for web deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(teacher.router)
app.include_router(student.router)

@app.get("/")
async def root():
    return {
        "message": "College Attendance System API",
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
    """Serve the frontend application"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    else:
        return {"message": "Frontend not found. Please check if static/index.html exists."}

if __name__ == "__main__":
    import uvicorn
    # Use environment variables for production
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port) 