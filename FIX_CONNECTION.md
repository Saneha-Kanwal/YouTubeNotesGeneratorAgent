# Fix Connection Errors

## Issues Fixed

1. ✅ **Hydration Warning**: Added `suppressHydrationWarning` to layout (browser extensions cause this)
2. ✅ **Connection Refused**: Backend not running - use commands below to start

## Quick Fix Commands

### Step 1: Initialize Database (if not done)

```bash
# Create database (if not exists)
PGPASSWORD=123456 psql -U postgres -h localhost -c "CREATE DATABASE youtube_notes;"

# Initialize schema
PGPASSWORD=123456 psql -U postgres -h localhost -d youtube_notes -f backend/db/schema.sql
```

### Step 2: Start Backend

**Option A: Use the start script (easiest)**
```bash
./START_BACKEND.sh
```

**Option B: Manual start**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make sure .env exists with your OpenAI API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Frontend (in another terminal)

```bash
cd frontend
npm run dev
```

## Verify Backend is Running

```bash
# Test backend health
curl http://localhost:8000/health

# Should return: {"status": "healthy", "database": "connected"}
```

## Common Issues

### "Connection refused" Error

**Cause**: Backend is not running on port 8000

**Solution**: 
1. Start the backend using commands above
2. Check if port 8000 is available: `lsof -i :8000`
3. Make sure backend/.env has correct DATABASE_URL

### "Failed to fetch" Error

**Cause**: Frontend can't reach backend API

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in backend (should allow localhost:3000)
3. Verify `NEXT_PUBLIC_API_BASE` in frontend/.env.local

### Hydration Warning

**Cause**: Browser extensions modifying HTML (like Liner, password managers, etc.)

**Solution**: Already fixed with `suppressHydrationWarning` in layout.tsx. This is harmless and won't affect functionality.

## Running Both Services

**Terminal 1 - Backend:**
```bash
./START_BACKEND.sh
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - View logs:**
```bash
# Backend logs will show in Terminal 1
# Frontend logs will show in Terminal 2
```

## Access Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

