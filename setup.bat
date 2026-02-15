@echo off
REM Breeze Trader Enhanced - Setup Script for Windows
REM Version: 8.5

echo ===============================================================
echo      Breeze Options Trader - Enhanced v8.5 Setup (Windows)
echo ===============================================================
echo.

REM Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found. Please install Python 3.8 or higher
    echo     Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [+] Python detected
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
if exist venv (
    echo [!] Virtual environment already exists
    choice /C YN /M "Remove and recreate"
    if errorlevel 2 goto skip_venv
    rmdir /s /q venv
)
python -m venv venv
echo [+] Virtual environment created
:skip_venv
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo [+] Virtual environment activated
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [+] pip upgraded
echo.

REM Install dependencies
echo [*] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [X] Failed to install dependencies
    pause
    exit /b 1
)
echo [+] Dependencies installed
echo.

REM Create directories
echo [*] Creating directories...
if not exist "data" mkdir data
if not exist ".streamlit" mkdir .streamlit
if not exist "logs" mkdir logs
echo [+] Directories created
echo.

REM Create secrets template
if not exist ".streamlit\secrets.toml" (
    echo [*] Creating secrets template...
    (
        echo # Breeze API Credentials
        echo # Get these from ICICI Breeze portal: https://api.icicidirect.com/apiuser/home
        echo.
        echo BREEZE_API_KEY = "your_api_key_here"
        echo BREEZE_API_SECRET = "your_api_secret_here"
        echo.
        echo # Note: Session token must be entered daily in the app
        echo # It expires every 24 hours
    ) > .streamlit\secrets.toml
    echo [+] Secrets template created at .streamlit\secrets.toml
    echo     [!] IMPORTANT: Edit this file with your API credentials
) else (
    echo [i] Secrets file already exists
)
echo.

REM Create Streamlit config
if not exist ".streamlit\config.toml" (
    echo [*] Creating Streamlit configuration...
    (
        echo [server]
        echo port = 8501
        echo headless = true
        echo.
        echo [browser]
        echo gatherUsageStats = false
        echo.
        echo [theme]
        echo primaryColor = "#1f77b4"
        echo backgroundColor = "#ffffff"
        echo secondaryBackgroundColor = "#f8f9fa"
        echo textColor = "#2c3e50"
        echo font = "sans serif"
    ) > .streamlit\config.toml
    echo [+] Streamlit configuration created
) else (
    echo [i] Streamlit config already exists
)
echo.

REM Verification
echo [*] Running setup verification...
python -c "import streamlit; import pandas; import numpy; from breeze_connect import BreezeConnect; print('[+] All packages verified')"
if errorlevel 1 (
    echo [X] Package verification failed
    pause
    exit /b 1
)
echo.

echo ===============================================================
echo                    Setup Complete! [OK]
echo ===============================================================
echo.
echo [*] Next Steps:
echo.
echo 1. Edit credentials:
echo    notepad .streamlit\secrets.toml
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
echo 3. Access in browser:
echo    http://localhost:8501
echo.
echo [*] Documentation:
echo    - README.md - User guide
echo    - REVIEW_REPORT.md - Technical details
echo.
echo [!] IMPORTANT NOTES:
echo    - Keep secrets.toml secure (never commit to git)
echo    - Get fresh session token daily from ICICI portal
echo    - Test with small orders first
echo    - Always use stop-losses
echo.
echo Happy Trading!
echo.
pause
