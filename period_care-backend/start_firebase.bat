@echo off
echo.
echo ========================================
echo   Period Care Backend - Firebase Setup
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

echo 📋 Installing dependencies (including Firebase)...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

REM Check if Firebase service account file exists
if not exist "firebase-service-account.json" (
    echo ⚠️ Firebase service account file not found!
    echo.
    echo Please follow these steps:
    echo 1. Go to https://console.firebase.google.com/
    echo 2. Create a new project or select existing project
    echo 3. Go to Project Settings ^> Service Accounts
    echo 4. Click "Generate new private key"
    echo 5. Download the JSON file and rename it to "firebase-service-account.json"
    echo 6. Place it in this directory: %CD%
    echo.
    echo Then run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Firebase service account file found
)

REM Check if .env file exists and has Firebase config
if not exist ".env" (
    echo ⚙️ Creating .env file with Firebase configuration...
    echo DATABASE_TYPE=firebase >> .env
    echo FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json >> .env
    echo FIREBASE_PROJECT_ID=your-firebase-project-id >> .env
    echo SECRET_KEY=your-secret-key-here-change-this-in-production >> .env
    echo ALGORITHM=HS256 >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
    echo REFRESH_TOKEN_EXPIRE_DAYS=7 >> .env
    echo ADMIN_WHATSAPP_NUMBER=+919999999999 >> .env
    echo FRONTEND_URL=http://localhost:5173 >> .env
    echo REMINDER_CHECK_TIME=09:00 >> .env
    echo DEBUG=True >> .env
    echo ENVIRONMENT=development >> .env
    echo.
    echo ⚠️ Please update FIREBASE_PROJECT_ID in .env file with your actual Firebase project ID
    pause
) else (
    echo ✅ Environment file found
)

echo.
echo 🔥 Initializing Firebase with sample data...
python init_firebase.py
if errorlevel 1 (
    echo ❌ Firebase initialization failed
    echo Please check your Firebase configuration and try again
    pause
    exit /b 1
)

echo ✅ Firebase initialized successfully
echo.

echo ========================================
echo       🚀 Starting Period Care API
echo ========================================
echo.
echo 🔥 Using Firebase Firestore Database
echo 📚 API Documentation: http://localhost:8000/docs
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
