#!/bin/bash
# Simple script to start both backend and frontend
# Opens two terminal windows (if available) or runs sequentially

echo "🚀 YouTube Notes AI Agent - Starting Both Servers"
echo "=================================================="
echo ""

# Check prerequisites
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed"
    exit 1
fi

# Check .env files
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating backend/.env..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your OPENAI_API_KEY"
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "⚠️  Creating frontend/.env.local..."
    echo "NEXT_PUBLIC_API_BASE=http://localhost:8000" > frontend/.env.local
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Try to use different methods to run both
if command_exists gnome-terminal; then
    # GNOME Terminal (Ubuntu/GNOME)
    echo "✅ Starting backend in new terminal..."
    gnome-terminal -- bash -c "cd $(pwd)/backend && export \$(cat .env | grep -v '^#' | xargs) && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; exec bash" &
    
    sleep 2
    
    echo "✅ Starting frontend in new terminal..."
    gnome-terminal -- bash -c "cd $(pwd)/frontend && npm run dev; exec bash" &
    
    echo ""
    echo "✅ Both servers started in separate terminals!"
    echo "📍 Backend:  http://localhost:8000"
    echo "📍 Frontend: http://localhost:3000"
    echo ""
    echo "Close the terminal windows to stop the servers"
    
elif command_exists xterm; then
    # xterm
    echo "✅ Starting backend in new terminal..."
    xterm -e "cd $(pwd)/backend && export \$(cat .env | grep -v '^#' | xargs) && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" &
    
    sleep 2
    
    echo "✅ Starting frontend in new terminal..."
    xterm -e "cd $(pwd)/frontend && npm run dev" &
    
    echo ""
    echo "✅ Both servers started in separate terminals!"
    
else
    # Fallback: Run in background in same terminal
    echo "⚠️  No terminal emulator found. Running both in background..."
    echo "   (Output will be mixed together)"
    echo ""
    
    cd backend
    export $(cat .env | grep -v '^#' | xargs)
    python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    sleep 3
    
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    echo "✅ Both servers started in background!"
    echo "📍 Backend:  http://localhost:8000 (PID: $BACKEND_PID)"
    echo "📍 Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
    echo ""
    echo "📋 View logs:"
    echo "   Backend:  tail -f backend.log"
    echo "   Frontend: tail -f frontend.log"
    echo ""
    echo "🛑 Stop servers:"
    echo "   kill $BACKEND_PID $FRONTEND_PID"
    echo ""
    
    # Wait for user interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    wait
fi

