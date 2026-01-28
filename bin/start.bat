@echo off
REM Start script for Windows

set SCRIPT_DIR=%~dp0
set PROJECT_DIR=%SCRIPT_DIR%..

cd /d "%PROJECT_DIR%"

REM Set environment
if not defined APP_ENV set APP_ENV=development
set PYTHONPATH=%PROJECT_DIR%;%PYTHONPATH%

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start the application
echo Starting Meilisearch Admin...
python -m backend.app
