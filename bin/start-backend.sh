#!/bin/bash
# Meilisearch Admin - Backend Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# Check Python environment
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
fi

# Start Flask backend
echo "Starting Meilisearch Admin Backend..."
echo "API Server: http://localhost:5000"

python -m backend.app
