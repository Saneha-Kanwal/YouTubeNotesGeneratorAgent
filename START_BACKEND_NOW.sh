#!/bin/bash
# Quick start script for backend server

cd "$(dirname "$0")/backend"

echo "🚀 Starting YouTube Notes AI Agent Backend"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "   Please create backend/.env file with your configuration"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY not set or using placeholder"
    echo "   Please edit backend/.env and add your OpenAI API key"
    echo ""
fi

# Check database connection
echo "🔍 Checking database connection..."
python3 << 'EOF'
import os
import sys
from dotenv import load_dotenv
load_dotenv()

try:
    import asyncpg
    import asyncio
    
    db_url = os.getenv('DATABASE_URL', '')
    if not db_url:
        print('❌ DATABASE_URL not set in .env')
        sys.exit(1)
    
    async def test_connection():
        try:
            conn = await asyncpg.connect(db_url)
            await conn.close()
            print('✅ Database connection successful')
            return True
        except Exception as e:
            print(f'❌ Database connection failed: {e}')
            print('   Please ensure PostgreSQL is running and DATABASE_URL is correct')
            return False
    
    if not asyncio.run(test_connection()):
        sys.exit(1)
except ImportError:
    print('⚠️  asyncpg not installed, skipping database check')
except Exception as e:
    print(f'⚠️  Error checking database: {e}')
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Database check failed. Please fix database connection before starting."
    exit 1
fi

echo ""
echo "🌐 Starting FastAPI server..."
echo "📍 Backend URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Start the server
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

