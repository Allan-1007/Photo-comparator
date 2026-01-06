@echo off
chcp 65001 >nul
echo 正在強制執行... (Force Running)

echo [1/3] 嘗試建立虛擬環境...
python -m venv venv

echo [2/3] 嘗試安裝套件...
venv\Scripts\python.exe -m pip install customtkinter Pillow imagehash

echo [3/3] 嘗試啟動...
venv\Scripts\python.exe main.py

echo.
echo 若上面出現錯誤，請截圖告知。
pause
