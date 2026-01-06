Write-Host "Checking Python..." -ForegroundColor Cyan
try {
    $ver = python --version 2>&1
    Write-Host "Found: $ver" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python command not found." -ForegroundColor Red
    Write-Host "Please install Python."
    Read-Host "Press Enter to exit"
    exit
}

if (-not (Test-Path "venv")) {
    Write-Host "Creating venv..." -ForegroundColor Cyan
    python -m venv venv
}

Write-Host "Activating venv..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing packages..." -ForegroundColor Cyan
pip install customtkinter Pillow imagehash

Write-Host "Starting App..." -ForegroundColor Cyan
python main.py

Read-Host "Press Enter to exit"
