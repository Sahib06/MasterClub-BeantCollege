#!/usr/bin/env python3
"""
Startup script for College Attendance System
This script will:
1. Install dependencies (if needed)
2. Seed the database with sample data
3. Start the FastAPI server
"""
import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"SUCCESS: {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import qrcode
        import pydantic
        print("SUCCESS: All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("College Attendance System - Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("college_attendance"):
        print("ERROR: Please run this script from the project root directory")
        print("Make sure you're in the directory containing the 'college_attendance' folder")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("\nInstalling dependencies...")
        if not run_command("pip install -r requirements.txt", "Installing dependencies"):
            return
    
    # Seed the database
    print("\nSetting up database...")
    if not run_command("python seed_data.py", "Seeding database"):
        print("WARNING: Database seeding failed, but continuing...")
    
    # Start the server
    print("\nStarting the server...")
    print("The application will be available at:")
    print("   - API Documentation: http://localhost:8000/docs")
    print("   - Frontend Interface: http://localhost:8000/ui")
    print("   - Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "college_attendance.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nServer error: {e}")

if __name__ == "__main__":
    main() 