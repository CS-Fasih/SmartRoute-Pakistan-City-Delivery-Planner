@echo off
cd /d "%~dp0smartroute"

if not exist venv\ (
    echo [ERROR] Virtual environment not found.
    echo         Please run setup_windows.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python main.py
call venv\Scripts\deactivate.bat >nul 2>&1
