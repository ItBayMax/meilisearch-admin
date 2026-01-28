#!/bin/bash
# Start script for Linux/Mac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Set environment
export APP_ENV=${APP_ENV:-development}
export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"

# Activate virtual environment if exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Start the application
echo "Starting Meilisearch Admin..."
python -m backend.app
