#!/bin/bash
# Quick start script for backend

cd "$(dirname "$0")/backend"

# Activate venv
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies if needed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Load environment
export $(cat .env | grep -v '^#' | xargs)

# Start server
echo "🚀 Starting FastAPI backend on http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

