@echo off
REM Groww Algo Trading - Run Script for Windows
REM This script starts both the backend (Flask) and serves the frontend

echo 🚀 Starting Groww Algo Trading Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Start the Flask server
echo.
echo ✅ Starting Flask server...
echo 🌐 The server will automatically find an available port
echo 📊 Look for the URL in the output above, then click 'Start Backtest'
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
