#!/bin/bash

# ===================================================================
# JEE RANK PREDICTOR - QUICK DEPLOYMENT COMMANDS
# ===================================================================
# This file contains all commands needed to deploy the project
# Copy and paste commands one by one in your terminal
# ===================================================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║    🚀 JEE RANK PREDICTOR - DEPLOYMENT COMMANDS               ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# ===================================================================
# STEP 1: PUSH TO GITHUB
# ===================================================================

echo ""
echo "📋 STEP 1: GITHUB PUSH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  First, create a repository at: https://github.com/new"
echo "   - Name it: jee-rank-predictor"
echo "   - Make it PUBLIC"
echo "   - Don't add README/gitignore"
echo ""
echo "2️⃣  Then run ONLY ONE of these (replace YOUR_USERNAME):"
echo ""
echo "   Via HTTPS (easier):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/jee-rank-predictor.git"
echo ""
echo "   Via SSH (if configured):"
echo "   git remote add origin git@github.com:YOUR_USERNAME/jee-rank-predictor.git"
echo ""
echo "3️⃣  Then push with:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "⏱️  Wait for upload to complete (1-2 minutes)"
echo ""

# ===================================================================
# STEP 2: DEPLOY BACKEND ON RENDER
# ===================================================================

echo "📋 STEP 2: RENDER BACKEND DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Go to: https://render.com"
echo ""
echo "2️⃣  Click: \"New +\" → \"Web Service\""
echo ""
echo "3️⃣  Connect your GitHub jee-rank-predictor repository"
echo ""
echo "4️⃣  Configure with these exact values:"
echo ""
echo "   ┌─────────────────────────────────────────────────────┐"
echo "   │ Name:            jee-rank-backend                   │"
echo "   │ Environment:     Python 3                           │"
echo "   │ Region:          Choose closest to you              │"
echo "   │ Branch:          main                               │"
echo "   │                                                     │"
echo "   │ Build Command:                                      │"
echo "   │ pip install -r requirements.txt                     │"
echo "   │                                                     │"
echo "   │ Start Command:                                      │"
echo "   │ uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"
echo "   │                                                     │"
echo "   │ Instance Type:   Free                               │"
echo "   └─────────────────────────────────────────────────────┘"
echo ""
echo "5️⃣  Click \"Advanced\" and add Environment Variables:"
echo ""
echo "   GEMINI_API_KEY = AIzaSyBaxFzgQ_MSmlfWAPsWu3V0GdAuYhUMJ1M"
echo "   GEMINI_MODEL = gemini-2.5-flash"
echo ""
echo "6️⃣  Click \"Create Web Service\" and WAIT 5-10 minutes"
echo ""
echo "✅ You'll get a URL like: https://jee-rank-backend.onrender.com"
echo ""

# ===================================================================
# STEP 3: DEPLOY FRONTEND ON VERCEL
# ===================================================================

echo "📋 STEP 3: VERCEL FRONTEND DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1️⃣  Go to: https://vercel.com"
echo ""
echo "2️⃣  Click: \"Add New...\" → \"Project\""
echo ""
echo "3️⃣  Click: \"Import Git Repository\""
echo ""
echo "4️⃣  Select: jee-rank-predictor"
echo ""
echo "5️⃣  Configure with these values:"
echo ""
echo "   ┌─────────────────────────────────────────────────────┐"
echo "   │ Framework Preset:    Other                          │"
echo "   │ Root Directory:      ./frontend                     │"
echo "   │ Build Command:       (leave empty)                  │"
echo "   │ Output Directory:    (leave empty)                  │"
echo "   │ Install Command:     (leave empty)                  │"
echo "   └─────────────────────────────────────────────────────┘"
echo ""
echo "6️⃣  Click \"Deploy\" and WAIT 2-5 minutes"
echo ""
echo "✅ You'll get a URL like: https://jee-rank-predictor.vercel.app"
echo ""

# ===================================================================
# STEP 4: VERIFY DEPLOYMENTS
# ===================================================================

echo "📋 STEP 4: VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Test Backend Health:"
echo "curl https://jee-rank-backend.onrender.com/api/health"
echo ""
echo "Test Prediction API:"
echo "curl -X POST https://jee-rank-backend.onrender.com/api/predict-rank \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"score\": 250, \"input_type\": \"marks\", \"year\": 2024, \"category\": \"GEN\"}'"
echo ""
echo "Test Frontend:"
echo "Visit: https://jee-rank-predictor.vercel.app"
echo ""

# ===================================================================
# FINAL LINKS
# ===================================================================

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                      📊 FINAL DEPLOYMENT LINKS               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 FRONTEND (Vercel):"
echo "   https://jee-rank-predictor.vercel.app"
echo ""
echo "🔌 BACKEND API (Render):"
echo "   https://jee-rank-backend.onrender.com"
echo ""
echo "📚 GITHUB REPOSITORY:"
echo "   https://github.com/YOUR_USERNAME/jee-rank-predictor"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✨ Everything is ready! Follow the steps above to deploy! ✨"
echo ""
