@echo off
title SmartRoute — Pakistan City Delivery Planner Setup
color 0B

echo ================================================================
echo          SmartRoute — Pakistan City Delivery Planner
echo          Setup Script for Windows
echo ================================================================
echo.

:: Step 1: Check Python installation
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo         Please install Python 3.9+ from https://www.python.org/downloads/
    echo         Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo         Found Python %%v
echo.

:: Step 2: Navigate to project directory
cd /d "%~dp0smartroute"
if %errorlevel% neq 0 (
    echo [ERROR] Could not find smartroute directory.
    pause
    exit /b 1
)

:: Step 3: Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv\ (
    echo         Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo         Virtual environment created successfully.
)
echo.

:: Step 4: Activate and install dependencies
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

echo [4/4] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo.

echo ================================================================
echo   Setup Complete!
echo ================================================================
echo.
echo   To run SmartRoute:
echo     1. Open a terminal in the smartroute folder
echo     2. Activate the virtual environment:
echo           venv\Scripts\activate
echo     3. Run:
echo           python main.py
echo.
echo   Or simply double-click: run_windows.bat
echo.
echo   Press any key to launch SmartRoute now...
pause >nul

python main.py

call venv\Scripts\deactivate.bat >nul 2>&1
