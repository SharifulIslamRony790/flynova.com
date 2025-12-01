@echo off
echo ========================================
echo FlyNova Project - Automatic Setup
echo ========================================
echo.

REM Check if venv already exists
if exist "venv\" (
    echo Virtual environment already exists.
    echo Deleting old venv to ensure clean install...
    rmdir /s /q venv
    echo.
)

echo [1/4] Creating fresh virtual environment...
python -m venv venv
if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment
    echo.
    echo Possible reasons:
    echo - Python is not installed
    echo - Python version is too old (need 3.10+)
    echo.
    echo Please install Python 3.10 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo ✓ Virtual environment created!
echo.

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated!
echo.

echo [3/4] Installing Django and dependencies...
echo This may take 1-2 minutes...
echo.
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo ✓ All dependencies installed!
echo.

echo [4/4] Setting up database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to setup database
    pause
    exit /b 1
)
echo ✓ Database ready!
echo.

echo ========================================
echo ✓ SETUP COMPLETE!
echo ========================================
echo.
echo Next step:
echo   Double-click: start_server.bat
echo.
echo Or run manually:
echo   venv\Scripts\activate
echo   python manage.py runserver 5000
echo.
echo ========================================
echo Admin Panel Access:
echo   URL: http://127.0.0.1:5000/admin/
echo   Username: admin
echo   Password: admin123
echo ========================================
echo.
pause
