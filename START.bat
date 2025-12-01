@echo off
REM ========================================
REM FlyNova - ZERO SETUP VERSION
REM ========================================

cls
echo.
echo ╔════════════════════════════════════════╗
echo ║         FlyNova Server                 ║
echo ╚════════════════════════════════════════╝
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found on this PC
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if packages installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo Installing packages (one-time, 2 minutes)...
    python -m pip install -r requirements.txt --quiet --user
    if errorlevel 1 (
        echo ❌ Installation failed
        pause
        exit /b 1
    )
)

REM Run migrations if needed
if not exist "db.sqlite3" (
    echo Setting up database...
    python manage.py migrate --noinput
)

REM Start server
echo.
echo ✓ Starting server...
echo.
echo ════════════════════════════════════════
echo   Server: http://127.0.0.1:5000/
echo   Admin:  http://127.0.0.1:5000/admin/
echo.
echo   Username: admin
echo   Password: admin123
echo ════════════════════════════════════════
echo.
echo Press Ctrl+C to stop
echo.

python manage.py runserver 5000
