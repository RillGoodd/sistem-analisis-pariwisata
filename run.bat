@echo off
REM ============================================
REM Sistem Analisis Pariwisata Indonesia
REM Quick Setup & Run Script
REM ============================================

echo.
echo ==============================================
echo   SISTEM ANALISIS PARIWISATA INDONESIA
echo ==============================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [1] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python 3.8+ is installed
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo [2] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Install requirements
echo [3] Installing dependencies...
echo (This may take 2-3 minutes on first run)
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Try: pip install -r requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Start application
echo [4] Starting application...
echo.
echo Browser will open automatically at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
streamlit run app.py

pause
