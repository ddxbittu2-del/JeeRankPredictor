# 🚀 Render Backend Deployment

Your frontend is live at: **https://frontend-teal-three-71.vercel.app**

Now deploy the backend to Render using these steps:

## Step 1: Go to Render Dashboard
👉 **https://dashboard.render.com**

## Step 2: Create New Web Service
1. Click the **"New +"** button (top-right)
2. Select **"Web Service"**

## Step 3: Connect GitHub Repository
1. Click **"Connect account"** if needed (authorize Render to access GitHub)
2. In the **"Repository"** field, search for: `JeeRankPredictor`
3. Click to select: `ddxbittu2-del/JeeRankPredictor`
4. Click **"Connect"**

## Step 4: Configure Service Settings
Fill in these exact values:

| Field | Value |
|-------|-------|
| **Name** | `jee-rank-backend` |
| **Root Directory** | `.` (leave empty or dot) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |
| **Region** | `Oregon` (or closest to you) |

## Step 5: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add **TWO** variables:

### Variable 1:
- **Key:** `GEMINI_API_KEY`
- **Value:** `AIzaSyBaxFzgQ_MSmlfWAPsWu3V0GdAuYhUMJ1M`

### Variable 2:
- **Key:** `GEMINI_MODEL`
- **Value:** `gemini-2.5-flash`

## Step 6: Deploy!
Click the blue **"Create Web Service"** button at the bottom.

⏱️ **Wait 5-10 minutes** for the backend to build and deploy.

## ✅ When Complete
You'll see:
- ✅ Status: "Available"
- 🔗 Live URL: `https://jee-rank-backend-XXXXX.onrender.com`

---

## 🧪 Test Your Backend

Once live, run these commands:

```bash
# Test health check
curl https://jee-rank-backend-XXXXX.onrender.com/api/health

# Test rank prediction
curl -X POST https://jee-rank-backend-XXXXX.onrender.com/api/predict-rank \
  -H 'Content-Type: application/json' \
  -d '{"score": 250, "input_type": "marks", "year": 2024, "category": "GEN"}'

# Test Gemini status
curl https://jee-rank-backend-XXXXX.onrender.com/api/gemini/status
```

Replace `XXXXX` with your actual service ID from the Render URL.

---

## �� Final URLs

| Service | URL |
|---------|-----|
| **Frontend** | https://frontend-teal-three-71.vercel.app |
| **Backend** | https://jee-rank-backend-XXXXX.onrender.com (get after deployment) |
| **GitHub** | https://github.com/ddxbittu2-del/JeeRankPredictor |

**Total deployment time: ~15 minutes from now** ⏱️  
**Total cost: $0/month forever** 💰

