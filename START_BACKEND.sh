#!/bin/bash
# Start backend server script

set -e

echo "🚀 Starting YouTube Notes AI Agent Backend"
echo "=========================================="
echo ""

cd "$(dirname "$0")/backend"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check database connection
echo "🔍 Checking database connection..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL', '')
if '123456' in db_url and 'localhost' in db_url:
    print('✅ Database configured for local PostgreSQL')
else:
    print('⚠️  Database URL:', db_url[:50] + '...')
" || echo "⚠️  Could not verify database configuration"

echo ""
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API docs will be available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

