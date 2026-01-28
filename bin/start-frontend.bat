@echo off
REM Meilisearch Admin - Frontend Dev Server Script

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set FRONTEND_DIR=%PROJECT_DIR%\frontend

cd /d "%FRONTEND_DIR%"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting Meilisearch Admin Frontend Dev Server...
echo Dev Server: http://localhost:8080

npm run dev
