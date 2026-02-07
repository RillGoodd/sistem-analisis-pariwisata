#!/bin/bash

# ============================================
# Sistem Analisis Pariwisata Indonesia
# Quick Setup & Run Script
# ============================================

echo ""
echo "=============================================="
echo "  SISTEM ANALISIS PARIWISATA INDONESIA"
echo "=============================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[1] Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        echo "Make sure Python 3.8+ is installed"
        exit 1
    fi
    echo "[OK] Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "[2] Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo "[OK] Virtual environment activated"
echo ""

# Install requirements
echo "[3] Installing dependencies..."
echo "(This may take 2-3 minutes on first run)"
python -m pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    echo "Try: pip install -r requirements.txt"
    exit 1
fi
echo "[OK] Dependencies installed"
echo ""

# Start application
echo "[4] Starting application..."
echo ""
echo "Browser will open automatically at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""
streamlit run app.py
