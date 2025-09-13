@echo off
echo.
echo ========================================
echo   Period Care - Background Tasks
echo ========================================
echo.

REM Activate virtual environment
if not exist "venv" (
    echo ❌ Virtual environment not found
    echo Please run start.bat first to set up the environment
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 🕐 Starting background task scheduler...
echo.
echo Tasks scheduled:
echo   • Daily reminder check: 09:00
echo   • Weekly cleanup: Sunday 02:00
echo.
echo Press Ctrl+C to stop the scheduler
echo.

REM Start the background task scheduler
python -m app.tasks.reminder_tasks

pause
