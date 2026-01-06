@echo off
echo Check venv...
if not exist "venv" (
    echo [Error] Virtual environment 'venv' not found. Please run run_force.bat first.
    pause
    exit /b
)

echo Activating venv...
call venv\Scripts\activate

echo Installing PyInstaller...
pip install pyinstaller

echo Cleaning up previous builds...
rmdir /s /q build dist 2>nul
del /q *.spec 2>nul

echo Building PhotoComparator.exe...
:: --collect-all customtkinter is CRITICAL for the UI library files
pyinstaller --noconsole --onefile --name "PhotoComparator" --collect-all customtkinter main.py

echo.
echo ========================================================
echo Build Complete!
echo You can find the executable in the 'dist' folder.
echo ========================================================
pause
