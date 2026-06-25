@echo off
title Fix PhishGuard Backend (Python 3.13)
cd /d "%~dp0"

echo Close any running python app.py windows first, then press any key...
pause >nul

echo Removing old venv...
rmdir /s /q venv 2>nul

echo Creating venv with Python 3.13 (required - NOT 3.14)...
py -3.13 -m venv venv

echo Installing packages...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Testing numpy...
venv\Scripts\python.exe -c "import numpy; print('NumPy OK:', numpy.__version__)"

echo.
echo Done! Run: venv\Scripts\python.exe app.py
pause
