#!/bin/bash
# Start script for YouTube Notes AI Agent with local PostgreSQL

set -e

echo "🚀 YouTube Notes AI Agent - Local PostgreSQL Setup"
echo "=================================================="
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY!"
    echo "   File location: backend/.env"
    echo ""
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend/.env.local from template..."
    cp frontend/.env.local.example frontend/.env.local
    echo "✅ Frontend .env.local created (defaults should work)"
    echo ""
fi

# Check if OpenAI API key is set
if grep -q "sk-your-openai-api-key-here" backend/.env 2>/dev/null; then
    echo "⚠️  WARNING: You need to edit backend/.env and add your actual OPENAI_API_KEY"
    echo "   Get your key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to edit .env first..."
fi

# Check if database exists
echo "🔍 Checking PostgreSQL connection..."
if psql -U postgres -h localhost -d youtube_notes -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database 'youtube_notes' exists and is accessible"
else
    echo "📊 Creating database 'youtube_notes'..."
    psql -U postgres -h localhost -c "CREATE DATABASE youtube_notes;" 2>/dev/null || {
        echo "⚠️  Database might already exist or connection failed"
        echo "   Please ensure PostgreSQL is running and password is correct"
    }
fi

# Initialize schema
echo ""
echo "📊 Initializing database schema..."
psql -U postgres -h localhost -d youtube_notes -f backend/db/schema.sql 2>/dev/null || {
    echo "⚠️  Schema might already be initialized, continuing..."
}

echo ""
echo "🐳 Starting Docker Compose services (backend + frontend only)..."
echo "   Note: Using your local PostgreSQL database"
docker-compose up -d

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📋 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""

