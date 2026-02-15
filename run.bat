@echo off
REM ═══════════════════════════════════════════════════════════════
REM Breeze Options Trader PRO - Windows Run Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║        Starting Breeze Options Trader PRO...             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo.
    echo Please run setup.bat first to install dependencies.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Streamlit app
echo Starting application...
echo.
echo ═══════════════════════════════════════════════════════════
echo   Application will open in your default browser
echo   Press Ctrl+C to stop the application
echo ═══════════════════════════════════════════════════════════
echo.

streamlit run app_enhanced.py

REM If streamlit exits, pause so user can see any errors
if errorlevel 1 (
    echo.
    echo ❌ Application exited with an error
    echo.
    pause
)
