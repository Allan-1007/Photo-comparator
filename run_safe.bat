@echo off
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b
    )
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements...
pip install customtkinter Pillow imagehash

echo Starting Application...
python main.py

echo Application closed.
pause
