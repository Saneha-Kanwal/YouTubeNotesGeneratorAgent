# Running with Local PostgreSQL Database

## Database Configuration

- **Host**: localhost
- **Port**: 5432
- **Database**: youtube_notes
- **User**: postgres
- **Password**: 123456

## Quick Start

### Step 1: Create Database (if not exists)

```bash
# Create the database
PGPASSWORD=123456 psql -U postgres -h localhost -c "CREATE DATABASE youtube_notes;"
```

### Step 2: Setup Environment Files

```bash
# Create .env files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local

# Edit backend/.env and add your OpenAI API key
nano backend/.env
# Set: OPENAI_API_KEY=sk-your-actual-key-here
```

The `backend/.env` file is already configured with:
```env
DATABASE_URL=postgresql://postgres:123456@localhost:5432/youtube_notes
```

### Step 3: Initialize Database Schema

```bash
# Run the schema
PGPASSWORD=123456 psql -U postgres -h localhost -d youtube_notes -f backend/db/schema.sql
```

### Step 4: Run the Application

**Option A: Use the start script**
```bash
./START_LOCAL_DB.sh
```

**Option B: Manual Docker Compose**
```bash
# Start backend and frontend (database runs locally)
docker-compose up -d

# View logs
docker-compose logs -f
```

**Option C: Manual Setup (No Docker)**

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env is already configured for local PostgreSQL
export OPENAI_API_KEY=sk-your-key-here

# Start backend
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Verify Database Connection

```bash
# Test connection
PGPASSWORD=123456 psql -U postgres -h localhost -d youtube_notes -c "SELECT COUNT(*) FROM videos;"

# Should return: count = 0 (empty, which is correct)
```

## Troubleshooting

### "Connection refused"
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if needed
sudo systemctl start postgresql
```

### "Database does not exist"
```bash
PGPASSWORD=123456 psql -U postgres -h localhost -c "CREATE DATABASE youtube_notes;"
```

### "Password authentication failed"
- Verify password is `123456`
- Try connecting manually: `psql -U postgres -h localhost`
- Check PostgreSQL `pg_hba.conf` if using peer authentication

### Docker can't connect to localhost PostgreSQL

The docker-compose.yml is configured to use `host.docker.internal` which allows Docker containers to access your localhost PostgreSQL. If this doesn't work:

1. Make sure PostgreSQL accepts connections from Docker network
2. Or run backend/frontend manually (not in Docker)

## Access Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

