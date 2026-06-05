# YouTube Notes AI Agent

A production-grade application that processes YouTube videos to generate structured study notes using AI.

## Features

- **Video Processing**: Download audio from YouTube videos and generate structured notes
- **AI-Powered Transcription**: Uses OpenAI Whisper for accurate transcription
- **Structured Notes**: Generates notes with headings, bullet points, key insights, quotes, and actionable takeaways
- **Multi-Language Support**: Translate notes into 50+ languages
- **History Tracking**: View and manage all processed videos

## UI 

<img width="1366" height="606" alt="image" src="https://github.com/user-attachments/assets/6f097071-0d13-4b49-86fd-00e70d718536" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/6d5e32e3-ab82-4f80-9342-0e78a9d6f7a5" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/f132929e-ea8e-4f00-ad2f-adb8b82562ba" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/e90cd3c4-84bf-4bcf-af4e-aa2fa7241bfa" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/623a056f-2472-4855-97a1-9ae537924852" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/4a278fc8-7776-4be0-83b3-464eff6f73fd" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/46f1800e-aadb-4f49-876f-4d9f1f09273b" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/8ffe1417-016e-4263-8338-48833e6110a8" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/f7b3767c-0325-4c5e-82a3-1f44e4c69350" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/dacff2cb-ca53-4e90-a09b-4dd6c6ae2104" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/77f5896f-87fb-4e05-850b-fd5bd98327a6" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/a960c498-48db-44a7-99cf-56978ba1176d" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/2374f2b8-aa96-448a-a07f-24ab7e2b567e" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/f90f8781-677a-4767-a337-3eb4b9301cb0" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/90de2bb5-7539-4450-9214-5a494d666b46" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/36b354b1-2978-4b2d-8e3d-3b747b815292" />
<img width="1366" height="604" alt="image" src="https://github.com/user-attachments/assets/22c1ffb2-bedf-48a9-b8a3-584ff1c4fab3" />



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

