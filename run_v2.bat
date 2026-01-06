@echo off
rem Switch to UTF-8 encoding
chcp 65001 >nul
setlocal

echo ==========================================
echo [1/5] 檢查 Python 環境 (Checking Python)...
echo ==========================================
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [錯誤 ERROR] 找不到 Python！ (Python not found)
    echo.
    echo 請前往 https://www.python.org/downloads/ 下載並安裝 Python。
    echo ★重要★ 安裝時請務必勾選 "Add Python to PATH"。
    echo.
    pause
    exit /b
)
python --version

echo.
echo ==========================================
echo [2/5] 清理舊環境 (Cleaning up)...
echo ==========================================
if exist venv (
    echo 正在刪除舊的 venv 資料夾...
    rmdir /s /q venv
)

echo.
echo ==========================================
echo [3/5] 建立虛擬環境 (Creating venv)...
echo ==========================================
python -m venv venv
if not exist "venv\Scripts\python.exe" (
    echo.
    echo [錯誤 ERROR] 虛擬環境建立失敗！
    echo 請確認您的 Python 安裝是否完整。
    echo.
    pause
    exit /b
)

echo.
echo ==========================================
echo [4/5] 安裝套件 (Installing packages)...
echo ==========================================
venv\Scripts\python.exe -m pip install customtkinter Pillow imagehash
if %errorlevel% neq 0 (
    echo.
    echo [錯誤 ERROR] 套件安裝失敗。請檢查網路連線。
    pause
    exit /b
)

echo.
echo ==========================================
echo [5/5] 啟動程式 (Starting App)...
echo ==========================================
venv\Scripts\python.exe main.py

echo.
echo 程式已結束。
pause
