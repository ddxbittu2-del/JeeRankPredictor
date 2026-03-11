#!/bin/bash

# JEE RANK PREDICTOR - AUTOMATED DEPLOYMENT SCRIPT
# This script will push your code to GitHub
# Render and Vercel deployments need to be done manually via their UI

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                    JEE RANK PREDICTOR DEPLOYMENT                           ║"
echo "║                                                                            ║"
echo "║            GitHub Push + Render & Vercel Deployment Guide                 ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if GitHub username provided
if [ -z "$1" ]; then
    echo "❌ GitHub username required!"
    echo ""
    echo "Usage: ./deploy.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example: ./deploy.sh tejasavayadav"
    echo ""
    exit 1
fi

GITHUB_USERNAME=$1
PROJECT_DIR="/Users/tejasavayadav/Desktop/jee rank pridictor"

cd "$PROJECT_DIR" || exit 1

echo "📍 Working directory: $PROJECT_DIR"
echo ""

# STEP 1: GitHub Setup
echo "════════════════════════════════════════════════════════════════════════════"
echo "STEP 1: GitHub Push (Automatic)"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Check if remote already exists
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists. Removing..."
    git remote remove origin
fi

echo "📝 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/jee-rank-predictor.git"

echo "📝 Setting branch to main..."
git branch -M main

echo "📤 Pushing to GitHub..."
echo ""
echo "⚠️  You will be prompted for your GitHub credentials"
echo "   If using personal access token, paste it as password when prompted"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ GitHub push successful!"
    echo ""
    echo "🔗 Your GitHub repository: https://github.com/$GITHUB_USERNAME/jee-rank-predictor"
else
    echo ""
    echo "❌ GitHub push failed. Check your credentials and try again."
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "STEP 2: Render Backend Deployment (Manual)"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Follow these steps to deploy on Render:"
echo ""
echo "1. Go to: https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Connect GitHub repository: jee-rank-predictor"
echo "5. Configure with these settings:"
echo ""
echo "   Name:            jee-rank-backend"
echo "   Environment:     Python 3"
echo "   Region:          Choose closest to you"
echo "   Build Command:   pip install -r requirements.txt"
echo "   Start Command:   uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"
echo ""
echo "6. Click 'Advanced' and add Environment Variables:"
echo ""
echo "   GEMINI_API_KEY = AIzaSyBaxFzgQ_MSmlfWAPsWu3V0GdAuYhUMJ1M"
echo "   GEMINI_MODEL = gemini-2.5-flash"
echo ""
echo "7. Click 'Create Web Service'"
echo "8. Wait 5-10 minutes for deployment"
echo ""
echo "✅ Your backend will be at: https://jee-rank-backend.onrender.com"
echo ""

echo "════════════════════════════════════════════════════════════════════════════"
echo "STEP 3: Vercel Frontend Deployment (Manual)"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Follow these steps to deploy on Vercel:"
echo ""
echo "1. Go to: https://vercel.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'Add New...' → 'Project'"
echo "4. Click 'Import Git Repository'"
echo "5. Select: jee-rank-predictor"
echo "6. Configure with these settings:"
echo ""
echo "   Framework Preset:  Other"
echo "   Root Directory:    ./frontend"
echo "   Build Command:     (leave empty)"
echo "   Output Directory:  (leave empty)"
echo ""
echo "7. Click 'Deploy'"
echo "8. Wait 2-5 minutes for deployment"
echo ""
echo "✅ Your frontend will be at: https://jee-rank-predictor.vercel.app"
echo ""

echo "════════════════════════════════════════════════════════════════════════════"
echo "STEP 4: Test Your Deployment"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "After both services are deployed, test them:"
echo ""
echo "Test backend health:"
echo "  curl https://jee-rank-backend.onrender.com/api/health"
echo ""
echo "Test prediction:"
echo "  curl -X POST https://jee-rank-backend.onrender.com/api/predict-rank \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"score\": 250, \"input_type\": \"marks\", \"year\": 2024, \"category\": \"GEN\"}'"
echo ""
echo "Visit frontend:"
echo "  https://jee-rank-predictor.vercel.app"
echo ""

echo "════════════════════════════════════════════════════════════════════════════"
echo "🎉 DEPLOYMENT COMPLETE!"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Your live links:"
echo ""
echo "  🌐 Frontend:   https://jee-rank-predictor.vercel.app"
echo "  🔌 Backend:    https://jee-rank-backend.onrender.com"
echo "  📚 GitHub:     https://github.com/$GITHUB_USERNAME/jee-rank-predictor"
echo ""
echo "Total cost per month: $0 (forever!) 🎉"
echo ""
