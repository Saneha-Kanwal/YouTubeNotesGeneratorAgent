#!/bin/bash
# Start both backend and frontend together
# This script runs both servers in the same terminal with colored output

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting YouTube Notes AI Agent (Backend + Frontend)${NC}"
echo "=========================================="
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠️  Creating backend/.env from template...${NC}"
    cp backend/.env.example backend/.env
    echo -e "${YELLOW}⚠️  IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY!${NC}"
    echo ""
fi

if [ ! -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}⚠️  Creating frontend/.env.local...${NC}"
    cp frontend/.env.local.example frontend/.env.local 2>/dev/null || echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > frontend/.env.local
    echo ""
fi

# Function to start backend
start_backend() {
    cd backend
    echo -e "${GREEN}🔧 Starting Backend Server...${NC}"
    echo -e "${BLUE}📍 Backend: http://localhost:8000${NC}"
    echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
    echo ""
    
    # Load environment variables
    export $(cat .env | grep -v '^#' | xargs)
    
    # Start backend
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Function to start frontend
start_frontend() {
    cd frontend
    echo -e "${GREEN}🎨 Starting Frontend Server...${NC}"
    echo -e "${BLUE}📍 Frontend: http://localhost:3000${NC}"
    echo ""
    
    # Start frontend
    npm run dev
}

# Check if we have the required tools
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

# Use a process manager approach: start both in background and wait
echo -e "${GREEN}Starting both servers...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""

# Start backend in background
(
    cd backend
    export $(cat .env | grep -v '^#' | xargs)
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 2>&1 | sed 's/^/[BACKEND] /'
) &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend in background
(
    cd frontend
    npm run dev 2>&1 | sed 's/^/[FRONTEND] /'
) &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}✅ Both servers are starting...${NC}"
echo ""
echo -e "${BLUE}📍 Backend:  http://localhost:8000${NC}"
echo -e "${BLUE}📍 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop both servers${NC}"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

