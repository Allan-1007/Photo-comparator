@echo off
echo 正在檢查 Python 環境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請確認您已安裝 Python 並加入環境變數 (PATH)。
    pause
    exit /b
)

if not exist "venv" (
    echo 正在建立虛擬環境...
    python -m venv venv
)

echo 正在啟動虛擬環境...
call venv\Scripts\activate

echo 正在安裝/檢查必要套件...
pip install customtkinter Pillow imagehash

echo 正在啟動照片比對程式...
python main.py

pause
