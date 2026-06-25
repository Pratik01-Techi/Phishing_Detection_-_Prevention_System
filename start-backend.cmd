@echo off
title PhishGuard Backend
cd /d "%~dp0backend"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment with Python 3.13...
    py -3.13 -m venv venv
)

echo Installing dependencies (if needed)...
venv\Scripts\python.exe -m pip install -r requirements.txt -q
echo.
echo Starting PhishGuard API on http://localhost:5000
echo Keep this window OPEN while using the app.
echo.
venv\Scripts\python.exe app.py
pause
