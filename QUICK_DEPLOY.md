# 🚀 Quick Deploy to Web

## **Step 1: Prepare Your Code**

Run this command to set up Git:
```bash
python deploy.py
```

## **Step 2: Choose Your Platform**

### **Option A: Railway (Recommended - 5 minutes)**

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Wait for deployment (2-3 minutes)
6. Your app will be live at: `https://your-app-name.railway.app`

### **Option B: Render (Free - 5 minutes)**

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn college_attendance.main:app --host 0.0.0.0 --port $PORT`
7. Click "Create Web Service"
8. Your app will be live at: `https://your-app-name.onrender.com`

## **Step 3: Test Your Deployment**

Once deployed, test these URLs:

- **Frontend**: `https://your-app.com/ui`
- **API Docs**: `https://your-app.com/docs`
- **Health Check**: `https://your-app.com/health`

## **Step 4: Use on Mobile**

### **For Teachers:**
1. Open your app URL on any device
2. Go to Teacher Dashboard
3. Generate QR codes for classes

### **For Students:**
1. Open your app URL on mobile phones
2. Go to Student Portal
3. Scan QR codes and mark attendance

## **🎉 Done!**

Your College Attendance System is now live on the web and accessible to students and teachers worldwide!

---

**Need help?** See `DEPLOYMENT_GUIDE.md` for detailed instructions. 