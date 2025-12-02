# Setup with Local PostgreSQL Database

## Prerequisites

- PostgreSQL installed and running locally
- Database name: `youtube_notes`
- Username: `postgres`
- Password: `123456`

## Step 1: Create Database (if not exists)

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE youtube_notes;

# Exit psql
\q
```

Or in one command:
```bash
psql -U postgres -c "CREATE DATABASE youtube_notes;"
```

## Step 2: Setup Environment Variables

```bash
# Create backend .env file
cp backend/.env.example backend/.env

# Edit backend/.env - it's already configured for local PostgreSQL:
# DATABASE_URL=postgresql://postgres:123456@localhost:5432/youtube_notes

# Add your OpenAI API key
nano backend/.env
# Set: OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Initialize Database Schema

```bash
# Run the schema SQL file
psql -U postgres -d youtube_notes -f backend/db/schema.sql
```

## Step 4: Run the Application

### Option A: Docker Compose (Backend + Frontend only)

```bash
# Start backend and frontend (database runs locally)
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option B: Manual Setup (No Docker)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# .env file is already configured for local PostgreSQL
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
psql -U postgres -d youtube_notes -c "SELECT COUNT(*) FROM videos;"

# Should return: count = 0 (empty table, which is correct)
```

## Database Configuration

**Current Settings:**
- Host: `localhost`
- Port: `5432` (PostgreSQL default)
- Database: `youtube_notes`
- User: `postgres`
- Password: `123456`

**Connection String:**
```
postgresql://postgres:123456@localhost:5432/youtube_notes
```

## Troubleshooting

### "Connection refused" error
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
# or
brew services list  # Mac

# Start PostgreSQL if not running
sudo systemctl start postgresql  # Linux
```

### "Database does not exist" error
```bash
# Create the database
psql -U postgres -c "CREATE DATABASE youtube_notes;"
```

### "Password authentication failed"
- Verify password is `123456`
- Check PostgreSQL authentication settings in `pg_hba.conf`
- Try: `psql -U postgres -h localhost` to test connection

### "Permission denied"
```bash
# Grant permissions (if needed)
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE youtube_notes TO postgres;"
```

## Access Application

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

