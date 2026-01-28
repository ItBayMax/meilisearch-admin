@echo off
REM Meilisearch Admin - Backend Start Script

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

cd /d "%PROJECT_DIR%"

REM Check Python virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo Starting Meilisearch Admin Backend...
echo API Server: http://localhost:5000

python -m backend.app
