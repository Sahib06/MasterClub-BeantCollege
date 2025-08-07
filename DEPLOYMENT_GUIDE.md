# 🌐 College Attendance System - Deployment Guide

## **Quick Deployment Options**

### **Option 1: Railway (Recommended - Easiest)**

1. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect Python and deploy

3. **Set Environment Variables**
   - Go to your project settings
   - Add environment variable: `DATABASE_URL = sqlite:///./college_attendance.db`

4. **Access Your App**
   - Railway will provide a URL like: `https://your-app-name.railway.app`
   - Your app will be live at this URL

### **Option 2: Render (Free Tier)**

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn college_attendance.main:app --host 0.0.0.0 --port $PORT`

3. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app

### **Option 3: Heroku (Professional)**

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Open Your App**
   ```bash
   heroku open
   ```

## **Mobile Access Setup**

### **For Students on Mobile:**

1. **Generate QR Code** (Teacher)
   - Teacher goes to your deployed URL
   - Generates QR code for class
   - Displays QR code to students

2. **Scan QR Code** (Students)
   - Students open the deployed URL on their phones
   - Click "Start Camera" to scan QR code
   - Enter their details and mark attendance

### **Example URLs:**
- **Railway**: `https://college-attendance-123.railway.app`
- **Render**: `https://college-attendance.onrender.com`
- **Heroku**: `https://your-app-name.herokuapp.com`

## **Environment Variables**

Set these in your deployment platform:

```env
DATABASE_URL=sqlite:///./college_attendance.db
PORT=8000
HOST=0.0.0.0
```

## **Database Setup**

The system will automatically:
1. Create database tables on first run
2. Seed sample data (teachers and students)
3. Be ready for use immediately

## **Security Considerations**

1. **CORS Settings**: Update `allow_origins` in `main.py` with your domain
2. **HTTPS**: All platforms provide HTTPS by default
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Authentication**: Add teacher login for production use

## **Testing Your Deployment**

1. **Health Check**: Visit `https://your-app.com/health`
2. **API Docs**: Visit `https://your-app.com/docs`
3. **Frontend**: Visit `https://your-app.com/ui`

## **Troubleshooting**

### **Common Issues:**

1. **Build Fails**
   - Check `requirements.txt` is complete
   - Ensure Python version is compatible

2. **App Won't Start**
   - Check environment variables
   - Verify `Procfile` or start command

3. **Database Issues**
   - Ensure `DATABASE_URL` is set correctly
   - Check file permissions for SQLite

### **Support:**
- Railway: Built-in support in dashboard
- Render: Documentation and community
- Heroku: Extensive documentation and support

## **Next Steps After Deployment**

1. **Customize Domain** (Optional)
   - Add custom domain in platform settings
   - Update CORS settings with your domain

2. **Add Authentication**
   - Implement teacher login system
   - Add student authentication if needed

3. **Monitor Usage**
   - Check platform analytics
   - Monitor database usage

4. **Scale Up** (If Needed)
   - Upgrade to paid plans for more resources
   - Add PostgreSQL for better performance

---

**🎉 Your College Attendance System will be live on the web and accessible to students and teachers worldwide!** 
