@echo off
REM ========================================
REM FlyNova - ONE-CLICK INSTALLER
REM ========================================

echo.
echo ╔════════════════════════════════════════╗
echo ║   FlyNova - Automatic Installation    ║
echo ╚════════════════════════════════════════╝
echo.
echo This will install everything automatically.
echo Please wait...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.10+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Clean old installation
if exist "venv\" (
    echo Removing old installation...
    rmdir /s /q venv
)

REM Create venv
echo [1/3] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate and install
echo [2/3] Installing packages (this may take 2-3 minutes)...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
)

REM Setup database
echo [3/3] Setting up database...
python manage.py migrate --noinput
if errorlevel 1 (
    echo ❌ Failed to setup database
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════╗
echo ║        ✓ INSTALLATION COMPLETE!       ║
echo ╚════════════════════════════════════════╝
echo.
echo To start the server:
echo   Double-click: RUN.bat
echo.
echo Or visit: http://127.0.0.1:5000/
echo.
pause
