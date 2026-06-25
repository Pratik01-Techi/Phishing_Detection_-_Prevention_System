# PhishGuard Backend — PowerShell launcher
Set-Location $PSScriptRoot\backend

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment with Python 3.13..."
    py -3.13 -m venv venv
}

Write-Host "Installing dependencies (if needed)..."
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt -q
Write-Host ""
Write-Host "Starting PhishGuard API on http://localhost:5000"
Write-Host "Keep this window OPEN while using the app."
Write-Host ""
& ".\venv\Scripts\python.exe" app.py
