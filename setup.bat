@echo off
REM ═══════════════════════════════════════════════════════════════
REM Breeze Options Trader PRO - Windows Setup Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   Breeze Options Trader PRO - Installation Script        ║
echo ║                 Windows Version                            ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
python --version
echo.

REM Check if virtual environment exists
if exist "venv" (
    echo ✓ Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo.
    echo Trying with verbose output...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Create necessary directories
echo Creating directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports
echo ✓ Directories created
echo.

REM Initialize database
echo Initializing database...
python -c "from persistence import TradeDB; db = TradeDB(); print('Database ready')"
if errorlevel 1 (
    echo ⚠️ Database initialization warning (non-critical)
) else (
    echo ✓ Database initialized
)
echo.

REM Configuration check
echo Checking configuration...
if exist "user_config.py" (
    echo ✓ User configuration found
) else (
    echo ⚠️ user_config.py not found - using defaults
)
echo.

echo ═══════════════════════════════════════════════════════════
echo   Installation Complete!
echo ═══════════════════════════════════════════════════════════
echo.
echo 🚀 To start the application, run:
echo.
echo     run.bat
echo.
echo Or manually with:
echo     venv\Scripts\activate
echo     streamlit run app_enhanced.py
echo.
echo 📚 For detailed documentation, see README.md
echo ═══════════════════════════════════════════════════════════
echo.
pause
