@echo off
echo.
echo ========================================
echo   Period Care Backend - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📋 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️ Environment file not found, using defaults...
    echo You may want to create a .env file for production settings
) else (
    echo ✅ Environment file found
)

echo.
echo 🗄️ Initializing database with sample data...
python init_db.py
if errorlevel 1 (
    echo ❌ Database initialization failed
    echo Make sure PostgreSQL is running and connection details are correct
    pause
    exit /b 1
)

echo ✅ Database initialized successfully
echo.

echo ========================================
echo       🚀 Starting Period Care API
echo ========================================
echo.
echo 📚 API Documentation will be available at:
echo    http://localhost:8000/docs
echo.
echo 🔑 Default Admin Login:
echo    Email: admin@periodcare.com
echo    Password: admin123
echo.
echo 👤 Test User Login:
echo    Email: priya@example.com
echo    Password: user123
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
