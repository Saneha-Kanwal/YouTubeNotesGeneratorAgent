# Running the YouTube Notes AI Agent

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

## Quick Start with Docker (Recommended)

### 1. Setup Environment Variables

```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY:
# OPENAI_API_KEY=sk-your-actual-key-here

# Frontend
cp frontend/.env.local.example frontend/.env.local
# Edit frontend/.env.local if needed (defaults should work)
```

### 2. Start All Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)

### 3. Initialize Database

```bash
# Wait for database to be ready (about 10 seconds)
sleep 10

# Run the schema
docker-compose exec db psql -U postgres -d youtube_notes -f /app/backend/db/schema.sql

# Or copy schema and run manually:
docker-compose exec db psql -U postgres -d youtube_notes < backend/db/schema.sql
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 5. View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 6. Stop Services

```bash
docker-compose down
```

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
export OPENAI_API_KEY=sk-your-key-here
export DATABASE_URL=postgresql://postgres:password@localhost:5432/youtube_notes
export FASTAPI_HOST=0.0.0.0
export FASTAPI_PORT=8000

# Make sure PostgreSQL is running and database exists
# Create database: createdb youtube_notes

# Run database schema
psql -U postgres -d youtube_notes -f db/schema.sql

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Generate Prisma client (for type safety)
npx prisma generate

# Set environment variables
export NEXT_PUBLIC_API_BASE=http://localhost:8000

# Start development server
npm run dev
```

## Development Commands

### Backend

```bash
cd backend

# Run with auto-reload
uvicorn app.main:app --reload

# Run with specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Check health
curl http://localhost:8000/health
```

### Frontend

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Database Management

### Access Database

```bash
# Via Docker
docker-compose exec db psql -U postgres -d youtube_notes

# Via local PostgreSQL
psql -U postgres -d youtube_notes
```

### Reset Database

```bash
# WARNING: This deletes all data
docker-compose down -v
docker-compose up -d db
# Wait for database to start
sleep 10
# Re-run schema
docker-compose exec db psql -U postgres -d youtube_notes -f /app/backend/db/schema.sql
```

## Troubleshooting

### Bootstrap CSS Not Found

If you see "Module not found: Can't resolve 'bootstrap/dist/css/bootstrap.min.css'":

```bash
cd frontend
npm install bootstrap bootstrap-icons
```

### Database Connection Errors

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database connection
docker-compose exec db psql -U postgres -c "SELECT 1"

# Verify DATABASE_URL format
# Should be: postgresql://postgres:password@db:5432/youtube_notes
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Or change ports in docker-compose.yml
```

### Frontend Build Errors

```bash
cd frontend
rm -rf node_modules .next
npm install
npm run build
```

## Testing the Application

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

### 2. Test Video Processing

```bash
curl -X POST http://localhost:8000/process-video \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

### 3. Test Frontend

1. Open http://localhost:3000
2. Enter a YouTube URL
3. Submit and wait for processing
4. View generated notes

## Production Deployment

For production, you'll need to:

1. Set up proper environment variables (use secrets management)
2. Configure CORS for your domain
3. Set up SSL/TLS certificates
4. Configure database backups
5. Set up monitoring and logging
6. Configure rate limiting
7. Set up CI/CD pipeline

See `quickstart.md` in `specs/001-youtube-notes-agent/` for more details.

