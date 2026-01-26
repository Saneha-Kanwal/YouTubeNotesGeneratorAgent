# Quickstart Guide

**Feature**: YouTube Notes AI Agent  
**Date**: 2025-01-27

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Git (for cloning repository)

## Quick Setup

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd YouTubeNotesGeneratorAgent
```

### 2. Environment Configuration

Create environment files from examples:

```bash
# Backend environment
cp backend/.env.example backend/.env

# Frontend environment
cp frontend/.env.local.example frontend/.env.local
```

Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
DATABASE_URL=postgresql://postgres:password@db:5432/youtube_notes
YT_DLP_BINARY=yt-dlp
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

### 3. Start Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)

### 4. Initialize Database

```bash
# Run database migrations (if using Alembic)
docker-compose exec backend alembic upgrade head

# Or create tables manually using SQL from data-model.md
docker-compose exec db psql -U postgres -d youtube_notes -f /path/to/schema.sql
```

### 5. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=sk-your-key
export DATABASE_URL=postgresql://postgres:password@localhost:5432/youtube_notes

# Run database migrations (if using Alembic)
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
export NEXT_PUBLIC_API_BASE=http://localhost:8000

# Generate Prisma client (for type safety, even though using raw queries)
npx prisma generate

# Start development server
npm run dev
```

## Verify Installation

### Test Backend

```bash
# Health check
curl http://localhost:8000/health

# Process a test video (replace with valid YouTube URL)
curl -X POST http://localhost:8000/process-video \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### Test Frontend

1. Open http://localhost:3000
2. Enter a YouTube URL
3. Submit and wait for processing
4. View generated notes

## Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services

```bash
docker-compose down
```

### Reset Database

```bash
# WARNING: This deletes all data
docker-compose down -v
docker-compose up -d
# Re-run migrations
```

### Access Database

```bash
docker-compose exec db psql -U postgres -d youtube_notes
```

## Development Workflow

### Backend Development

1. Make changes to Python files in `backend/app/`
2. FastAPI auto-reloads on file changes (if `--reload` flag used)
3. Check logs for errors: `docker-compose logs -f backend`

### Frontend Development

1. Make changes to TypeScript/React files in `frontend/`
2. Next.js hot-reloads automatically
3. Check browser console and terminal for errors

### Database Changes

1. Update SQL schema in `data-model.md`
2. Create migration script or update Alembic migration
3. Run migration: `alembic upgrade head` or execute SQL directly

## Troubleshooting

### Backend won't start

- Check OpenAI API key is set correctly
- Verify database connection string
- Ensure yt-dlp is installed: `which yt-dlp`
- Check logs: `docker-compose logs backend`

### Frontend can't connect to backend

- Verify `NEXT_PUBLIC_API_BASE` matches backend URL
- Check CORS settings in FastAPI (should allow localhost:3000)
- Verify backend is running: `curl http://localhost:8000/health`

### Database connection errors

- Verify PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL format
- Ensure database exists: `docker-compose exec db psql -U postgres -l`

### Video processing fails

- Check OpenAI API key is valid and has credits
- Verify YouTube URL is accessible
- Check yt-dlp can download: `yt-dlp --version`
- Review backend logs for specific error messages

## Next Steps

- Review [data-model.md](./data-model.md) for database schema
- Review [contracts/api.yaml](./contracts/api.yaml) for API endpoints
- Review [research.md](./research.md) for technical decisions
- Proceed to implementation tasks

