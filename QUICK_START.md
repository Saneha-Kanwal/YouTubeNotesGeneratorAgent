# Quick Start Guide

## 🚀 Fastest Way to Run (Docker Compose)

### Step 1: Setup Environment Variables

```bash
# Create .env files from templates
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit backend/.env and add your OpenAI API key
nano backend/.env
# or
code backend/.env
```

**In `backend/.env`, replace:**
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

### Step 2: Run the Application

**Option A: Use the start script (easiest)**
```bash
./START.sh
```

**Option B: Manual commands**
```bash
# Start all services
docker-compose up -d

# Wait for database (10 seconds)
sleep 10

# Initialize database
docker-compose exec -T db psql -U postgres -d youtube_notes < backend/db/schema.sql

# View logs
docker-compose logs -f
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs

---

## 📋 Manual Setup (Without Docker)

### Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Set environment variables
export OPENAI_API_KEY=sk-your-key-here
export DATABASE_URL=postgresql://postgres:password@localhost:5432/youtube_notes

# Make sure PostgreSQL is running, then initialize database
psql -U postgres -d youtube_notes -f db/schema.sql

# Start backend
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies (if not done)
npm install

# Create .env.local (defaults usually work)
cp .env.local.example .env.local

# Clear Next.js cache (if you had errors)
rm -rf .next

# Start frontend
npm run dev
```

---

## 🛠️ Troubleshooting

### Tailwind Error Fixed
- ✅ Removed Tailwind PostCSS config
- ✅ Created minimal postcss.config.js
- ✅ Cleared Next.js cache

### If you still see errors:

```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000  # Linux/Mac
# or
netstat -ano | findstr :8000  # Windows

# Kill the process or change ports in docker-compose.yml
```

---

## 📁 Environment File Locations

| File | Location | What to Add |
|------|----------|-------------|
| **Backend .env** | `backend/.env` | `OPENAI_API_KEY=sk-...` |
| **Frontend .env.local** | `frontend/.env.local` | Usually no changes needed |

---

## ✅ Verify Everything Works

### Test Backend
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

### Test Frontend
Open http://localhost:3000 in your browser

### Test Full Flow
1. Go to http://localhost:3000
2. Paste a YouTube URL
3. Click "Generate Notes"
4. Wait for processing
5. View generated notes

---

## 🛑 Stop the Application

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v
```

