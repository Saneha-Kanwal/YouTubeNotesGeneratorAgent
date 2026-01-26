# Environment Variables Setup Guide

## Backend Environment Variables

**Location**: `backend/.env`

### Step 1: Create the .env file

```bash
# Copy the example file
cp backend/.env.example backend/.env

# Or create it manually
touch backend/.env
```

### Step 2: Edit backend/.env

Open `backend/.env` and add your values:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# Database Configuration
# For Docker Compose (default):
DATABASE_URL=postgresql://postgres:password@db:5432/youtube_notes

# For local development (if running PostgreSQL locally):
# DATABASE_URL=postgresql://postgres:your_password@localhost:5432/youtube_notes

# YouTube Downloader
YT_DLP_BINARY=yt-dlp

# FastAPI Server Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

### Important Notes:

1. **OPENAI_API_KEY**: Get this from https://platform.openai.com/api-keys
   - Format: `sk-...` (starts with "sk-")
   - Keep this secret! Never commit to git.

2. **DATABASE_URL**: 
   - **For Docker**: Use `postgresql://postgres:password@db:5432/youtube_notes`
   - **For Local**: Use `postgresql://postgres:your_password@localhost:5432/youtube_notes`
   - Replace `your_password` with your actual PostgreSQL password

3. **Database Password**: 
   - In Docker Compose, the default password is `password` (see docker-compose.yml)
   - For production, change this in docker-compose.yml and .env

---

## Frontend Environment Variables

**Location**: `frontend/.env.local`

### Step 1: Create the .env.local file

```bash
# Copy the example file
cp frontend/.env.local.example frontend/.env.local

# Or create it manually
touch frontend/.env.local
```

### Step 2: Edit frontend/.env.local

Open `frontend/.env.local` and add:

```env
# API Base URL
# For Docker Compose (default):
NEXT_PUBLIC_API_BASE=http://localhost:8000

# For production:
# NEXT_PUBLIC_API_BASE=https://your-api-domain.com
```

### Important Notes:

- `NEXT_PUBLIC_` prefix is required for Next.js to expose the variable to the browser
- For Docker Compose, use `http://localhost:8000` (backend runs on port 8000)
- For production, use your actual API domain

---

## Quick Setup Commands

### Complete Setup (Copy and Run):

```bash
# Navigate to project root
cd /home/sanehakanwal/Documents/fista/YouTubeNotesGeneratorAgent

# Backend .env
cp backend/.env.example backend/.env
# Then edit backend/.env and add your OPENAI_API_KEY

# Frontend .env.local
cp frontend/.env.local.example frontend/.env.local
# Edit if needed (defaults should work for Docker)
```

### Edit the files:

```bash
# Edit backend .env (add your OpenAI API key)
nano backend/.env
# or
code backend/.env

# Edit frontend .env.local (usually no changes needed)
nano frontend/.env.local
# or
code frontend/.env.local
```

---

## Security Best Practices

1. **Never commit .env files to git**
   - They are already in .gitignore
   - Always use .env.example as a template

2. **Use different keys for development and production**
   - Development: Use test API keys
   - Production: Use production API keys with proper rate limits

3. **Rotate keys regularly**
   - If a key is exposed, regenerate it immediately
   - Update all .env files that use it

4. **Use environment-specific values**
   - Development: localhost URLs
   - Production: actual domain URLs

---

## Verification

After setting up .env files, verify they work:

### Backend:
```bash
cd backend
source venv/bin/activate  # if using venv
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"
```

### Frontend:
```bash
cd frontend
npm run dev
# Check browser console for NEXT_PUBLIC_API_BASE value
```

---

## Troubleshooting

### "OPENAI_API_KEY not set"
- Check that `backend/.env` exists
- Verify the key starts with `sk-`
- Make sure you're running from the backend directory or using Docker

### "Cannot connect to database"
- Check `DATABASE_URL` format
- Verify PostgreSQL is running
- For Docker: Check `docker-compose ps` to see if db service is up
- For local: Check `pg_isready` or `systemctl status postgresql`

### "API calls fail"
- Verify `NEXT_PUBLIC_API_BASE` in `frontend/.env.local`
- Check CORS settings in backend (should allow localhost:3000)
- Verify backend is running on the correct port

