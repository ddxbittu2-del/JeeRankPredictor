#!/bin/bash

# JEE Predictor Quick Start Script
# Run this to set up everything locally

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     JEE RANK & COLLEGE PREDICTOR - QUICK START           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅  Python $python_version"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅  Virtual environment created"
else
    echo "✅  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✅  Virtual environment activated"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅  Dependencies installed"
echo ""

# Download data
echo "📥 Downloading JoSAA data..."
echo "   (Using synthetic fallback if download fails)"
python scripts/download_data.py --synthetic
echo "✅  Data ready"
echo ""

# Train models
echo "🤖 Training ML models..."
python scripts/train_model.py
echo "✅  Models trained"
echo ""

# Print next steps
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1️⃣  Start the backend API:"
echo "   uvicorn backend.main:app --reload"
echo ""
echo "2️⃣  In another terminal, start a web server:"
echo "   cd frontend && python -m http.server 8001"
echo ""
echo "3️⃣  Open in browser:"
echo "   http://localhost:8001"
echo ""
echo "✨ That's it! The predictor is ready to use."
echo ""
echo "📚 For more info, see README.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
