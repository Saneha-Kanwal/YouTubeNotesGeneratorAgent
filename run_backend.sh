#!/bin/bash
# Start backend server (using system Python)

cd "$(dirname "$0")/backend"

echo "🚀 Starting YouTube Notes AI Agent Backend"
echo "=========================================="
echo ""

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env from template..."
    cp .env.example .env
    echo "✅ Please ensure OPENAI_API_KEY is set in .env"
    echo ""
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check database connection
echo "🔍 Checking database connection..."
python3 << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv('DATABASE_URL', '')
if 'localhost' in db_url and 'youtube_notes' in db_url:
    print('✅ Database configured correctly')
else:
    print(f'⚠️  Database URL: {db_url[:60]}...')
EOF

echo ""
echo "🌐 Starting FastAPI server..."
echo "📍 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

