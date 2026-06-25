@echo off
title PhishGuard Frontend
cd /d "%~dp0frontend"

if not exist "node_modules\vite\bin\vite.js" (
    echo Installing npm packages...
    call npm.cmd install
)

echo.
echo Starting dashboard on http://localhost:3000
echo Backend must be running first - use start-backend.cmd
echo.
node "%~dp0frontend\node_modules\vite\bin\vite.js"
pause
