# YouTube Notes AI Agent

A production-grade application that processes YouTube videos to generate structured study notes using AI.

## Features

- **Video Processing**: Download audio from YouTube videos and generate structured notes
- **AI-Powered Transcription**: Uses OpenAI Whisper for accurate transcription
- **Structured Notes**: Generates notes with headings, bullet points, key insights, quotes, and actionable takeaways
- **Multi-Language Support**: Translate notes into 50+ languages
- **History Tracking**: View and manage all processed videos

## Tech Stack

- **Frontend**: Next.js 15 (App Router), React 19, TypeScript, Bootstrap 5
- **Backend**: FastAPI (Python 3.11+), Uvicorn
- **Database**: PostgreSQL 15+
- **AI**: OpenAI API (Whisper for transcription, GPT for note generation and translation)

## Quick Start

### Prerequisites

- PostgreSQL 15+ (running locally)
- OpenAI API key
- Node.js 18+
- Python 3.11+

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd YouTubeNotesGeneratorAgent
```

2. Set up PostgreSQL database:
```bash
# Create database
PGPASSWORD=123456 psql -h localhost -U postgres -c "CREATE DATABASE youtube_notes;"

# Initialize schema
PGPASSWORD=123456 psql -h localhost -U postgres -d youtube_notes -f backend/db/schema.sql
```

3. Configure environment variables:
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your OPENAI_API_KEY

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

4. Start backend:
```bash
cd backend
bash ../run_backend.sh
```

5. Start frontend (in a new terminal):
```bash
cd frontend
npm install
npm run dev
```

6. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development

See [quickstart.md](specs/001-youtube-notes-agent/quickstart.md) for detailed development setup instructions.

## Project Structure

```
youtube-notes-agent/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
└── README.md
```

## License

[Add your license here]

