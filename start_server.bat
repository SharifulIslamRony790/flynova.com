@echo off
echo ========================================
echo FlyNova Server - Starting...
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run setup.bat first to install everything.
    echo.
    echo Steps:
    echo   1. Double-click: setup.bat
    echo   2. Wait for setup to complete
    echo   3. Then run this file again
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo ERROR: Django is not installed!
    echo.
    echo Please run setup.bat to install dependencies.
    echo.
    pause
    exit /b 1
)

echo Starting server on http://127.0.0.1:5000/
echo.
echo ========================================
echo Server is running!
echo ========================================
echo.
echo Open your browser and visit:
echo   http://127.0.0.1:5000/
echo.
echo Admin Panel:
echo   http://127.0.0.1:5000/admin/
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver 5000
