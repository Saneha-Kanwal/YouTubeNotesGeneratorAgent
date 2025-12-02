#!/bin/bash
# Quick start script for YouTube Notes AI Agent

set -e

echo "🚀 YouTube Notes AI Agent - Setup & Start"
echo "=========================================="
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

echo "🐳 Starting Docker Compose services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for database to be ready (10 seconds)..."
sleep 10

echo ""
echo "📊 Initializing database schema..."
docker-compose exec -T db psql -U postgres -d youtube_notes < backend/db/schema.sql 2>/dev/null || {
    echo "⚠️  Database might already be initialized, continuing..."
}

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

