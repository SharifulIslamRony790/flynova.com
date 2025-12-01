@echo off
REM ========================================
REM FlyNova - ONE-CLICK RUN
REM ========================================

REM Check if installed
if not exist "venv\Scripts\python.exe" (
    echo.
    echo ╔════════════════════════════════════════╗
    echo ║     Please Install First!              ║
    echo ╚════════════════════════════════════════╝
    echo.
    echo Double-click: INSTALL.bat
    echo.
    pause
    exit /b 1
)

REM Start server
cls
echo.
echo ╔════════════════════════════════════════╗
echo ║      FlyNova Server Starting...       ║
echo ╚════════════════════════════════════════╝
echo.
echo Server: http://127.0.0.1:5000/
echo Admin:  http://127.0.0.1:5000/admin/
echo.
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop
echo ════════════════════════════════════════
echo.

call venv\Scripts\activate.bat
python manage.py runserver 5000
