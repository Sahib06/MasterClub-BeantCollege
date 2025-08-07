#!/usr/bin/env python3
"""
Deployment helper script for College Attendance System
"""
import os
import subprocess
import sys

def check_git():
    """Check if git is available and repository is initialized"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository found")
            return True
        else:
            print("❌ Git repository not found")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def init_git():
    """Initialize git repository if not already done"""
    try:
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git initialization failed: {e}")
        return False

def create_github_repo():
    """Guide user to create GitHub repository"""
    print("\n📋 To deploy your app, you need to:")
    print("1. Create a GitHub repository")
    print("2. Push your code to GitHub")
    print("3. Deploy using one of the platforms below")
    
    print("\n🌐 Deployment Options:")
    print("Option 1: Railway (Easiest)")
    print("  - Go to https://railway.app")
    print("  - Sign up with GitHub")
    print("  - Click 'New Project' → 'Deploy from GitHub repo'")
    print("  - Select your repository")
    
    print("\nOption 2: Render (Free)")
    print("  - Go to https://render.com")
    print("  - Sign up with GitHub")
    print("  - Click 'New +' → 'Web Service'")
    print("  - Connect your GitHub repository")
    
    print("\nOption 3: Heroku (Professional)")
    print("  - Install Heroku CLI")
    print("  - Run: heroku create your-app-name")
    print("  - Run: git push heroku main")

def main():
    print("🚀 College Attendance System - Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("college_attendance"):
        print("❌ Error: Please run this script from the project root directory")
        return
    
    # Check git status
    if not check_git():
        print("\n📝 Initializing Git repository...")
        if not init_git():
            print("❌ Failed to initialize Git repository")
            return
    
    # Show deployment options
    create_github_repo()
    
    print("\n📚 For detailed instructions, see DEPLOYMENT_GUIDE.md")
    print("🎯 Your app will be accessible on mobile devices once deployed!")

if __name__ == "__main__":
    main() 