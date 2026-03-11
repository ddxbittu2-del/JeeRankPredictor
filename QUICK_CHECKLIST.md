# 📋 Quick Deployment Checklist

Copy and paste this checklist to track your deployment progress:

## ✅ Pre-Deployment (COMPLETE)
- [x] Project initialized with Git
- [x] All code committed
- [x] Render configuration ready
- [x] Vercel configuration ready
- [x] Environment variables configured
- [x] Gemini API key added

## 🔄 Deployment Steps

### Step 1: GitHub Push
**Time: ~2 minutes**

- [ ] Go to https://github.com/new
- [ ] Create repository `jee-rank-predictor` (PUBLIC)
- [ ] Copy HTTPS URL

Run these commands:
```bash
git remote add origin https://github.com/YOUR_USERNAME/jee-rank-predictor.git
git branch -M main
git push -u origin main
```

✅ Done when: All files appear on GitHub

---

### Step 2: Deploy Backend (Render)
**Time: ~7 minutes**

- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Select `jee-rank-predictor` repository
- [ ] Fill in configuration:
  - Name: `jee-rank-backend`
  - Environment: `Python 3`
  - Build: `pip install -r requirements.txt`
  - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add Environment Variables:
  - `GEMINI_API_KEY`: `AIzaSyBaxFzgQ_MSmlfWAPsWu3V0GdAuYhUMJ1M`
  - `GEMINI_MODEL`: `gemini-2.5-flash`
- [ ] Click "Create Web Service"

✅ Done when: Deployment shows "Live" and URL is: `https://jee-rank-backend.onrender.com`

Test it:
```bash
curl https://jee-rank-backend.onrender.com/api/health
```

---

### Step 3: Deploy Frontend (Vercel)
**Time: ~4 minutes**

- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "Add New..." → "Project"
- [ ] Click "Import Git Repository"
- [ ] Select `jee-rank-predictor`
- [ ] Fill in configuration:
  - Framework: `Other`
  - Root Directory: `./frontend`
  - Build Command: (leave empty)
  - Output Directory: (leave empty)
- [ ] Click "Deploy"

✅ Done when: Deployment completes and URL is: `https://jee-rank-predictor.vercel.app`

Visit it:
```
https://jee-rank-predictor.vercel.app
```

---

## 🎉 Deployment Complete!

### Your Live Links:

**Frontend (Vercel):**
```
https://jee-rank-predictor.vercel.app
```

**Backend API (Render):**
```
https://jee-rank-backend.onrender.com
```

**GitHub Repository:**
```
https://github.com/YOUR_USERNAME/jee-rank-predictor
```

---

## 📊 Testing Checklist

- [ ] Backend health check: `curl https://jee-rank-backend.onrender.com/api/health`
- [ ] Prediction test: `curl -X POST https://jee-rank-backend.onrender.com/api/predict-rank -H "Content-Type: application/json" -d '{"score": 250, "input_type": "marks", "year": 2024, "category": "GEN"}'`
- [ ] Frontend loads: Visit https://jee-rank-predictor.vercel.app
- [ ] Can predict rank on frontend
- [ ] AI features work (Smart Filter, Career Advisor, etc.)
- [ ] Gemini status: `curl https://jee-rank-backend.onrender.com/api/gemini/status`

---

## 🆘 Troubleshooting

**Issue: Backend deployment fails**
- Check build logs in Render dashboard
- Verify all packages in requirements.txt exist
- Ensure Python version is 3.11+

**Issue: Frontend can't connect to backend**
- Check if backend is running (curl health endpoint)
- Verify backend URL in frontend/app.js (should be production URL)
- Check browser console for CORS errors

**Issue: Gemini features not working**
- Verify API key is set in Render environment
- Check backend logs for Gemini errors
- Ensure internet connection is available

---

## 📈 After Deployment

### Monitor Backend
- Visit Render dashboard: https://dashboard.render.com
- Select your service
- View logs, metrics, and analytics

### Monitor Frontend
- Visit Vercel dashboard: https://vercel.com/dashboard
- Select your project
- View analytics and performance

### Update Code
After making changes:
```bash
git add .
git commit -m "Your change description"
git push origin main
```

Services auto-redeploy from GitHub!

---

## 🎯 Success Indicators

✨ Backend is running: Shows "Live" on Render dashboard
✨ Frontend is running: Shows "Ready" on Vercel dashboard
✨ API health check returns status: ok
✨ Frontend loads without errors
✨ Can predict ranks and get colleges
✨ AI features provide responses

---

**Status**: Ready to deploy! Follow the steps above. 🚀
