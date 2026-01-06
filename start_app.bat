@echo off
chcp 65001 >nul
echo 正在啟動...
if not exist venv (
    echo 正在建立環境...
    python -m venv venv
    venv\Scripts\python.exe -m pip install customtkinter Pillow imagehash
)
venv\Scripts\python.exe main.py
pause
