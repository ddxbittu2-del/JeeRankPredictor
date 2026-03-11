@echo off
REM JEE Predictor Quick Start Script for Windows
REM Run this to set up everything locally

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     JEE RANK ^& COLLEGE PREDICTOR - QUICK START           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check Python version
echo 📋 Checking Python version...
python --version
echo ✅  Python found
echo.

REM Create virtual environment
echo 🔧 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅  Virtual environment created
) else (
    echo ✅  Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅  Virtual environment activated
echo.

REM Install dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt
echo ✅  Dependencies installed
echo.

REM Download data
echo 📥 Downloading JoSAA data...
echo.    (Using synthetic fallback if download fails)
python scripts\download_data.py --synthetic
echo ✅  Data ready
echo.

REM Train models
echo 🤖 Training ML models...
python scripts\train_model.py
echo ✅  Models trained
echo.

REM Print next steps
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🎉 Setup complete! Next steps:
echo.
echo 1️⃣  Start the backend API:
echo    uvicorn backend.main:app --reload
echo.
echo 2️⃣  In another terminal, start a web server:
echo    cd frontend
echo    python -m http.server 8001
echo.
echo 3️⃣  Open in browser:
echo    http://localhost:8001
echo.
echo ✨ That's it! The predictor is ready to use.
echo.
echo 📚 For more info, see README.md
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
