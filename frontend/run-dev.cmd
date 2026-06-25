@echo off
cd /d "%~dp0"
if not exist "node_modules\vite\bin\vite.js" (
    echo Installing packages...
    call npm.cmd install
)
echo Starting http://localhost:3000
node "%~dp0node_modules\vite\bin\vite.js"
pause
