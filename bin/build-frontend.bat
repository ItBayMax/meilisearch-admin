@echo off
REM Meilisearch Admin - Frontend Build Script

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..
set FRONTEND_DIR=%PROJECT_DIR%\frontend

cd /d "%FRONTEND_DIR%"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Building Meilisearch Admin Frontend...

npm run build

echo Build completed! Output: frontend\dist\
