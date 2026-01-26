# 📁 Project Structure Documentation

## Industry-Standard Folder Organization

This project follows industry best practices for full-stack application structure.

---

## 🏗️ Root Structure

```
YouTubeNotesGeneratorAgent/
├── backend/              # Backend API server (Python/FastAPI)
├── frontend/             # Frontend application (Next.js/React)
├── specs/                # Project specifications and documentation
├── README.md             # Main project documentation
└── PROJECT_STRUCTURE.md  # This file
```

---

## 🔧 Backend Structure (`backend/`)

```
backend/
├── app/                  # Main application package
│   ├── __init__.py       # Package initialization
│   │
│   ├── main.py           # FastAPI application & API routes
│   ├── worker.py         # Background processing tasks
│   ├── openai_client.py  # OpenAI API wrapper (Agents SDK)
│   ├── schemas.py        # Pydantic request/response models
│   ├── utils.py          # Utility functions (URL validation, etc.)
│   │
│   ├── youtube_downloader.py  # YouTube audio downloader
│   ├── video_chunker.py       # Video chunking for long videos
│   ├── audio_chunker.py       # Audio file chunking utility
│   │
│   ├── db/               # Database layer
│   │   ├── __init__.py
│   │   ├── models.py     # SQLAlchemy models (reference)
│   │   └── crud.py       # Database CRUD operations (asyncpg)
│   │
│   └── lib/              # Shared libraries
│       ├── __init__.py
│       └── languages.py  # Supported languages definitions
│
├── db/                   # Database scripts
│   └── schema.sql        # PostgreSQL schema
│
├── audio_cache/          # Temporary audio file storage
│                         # (gitignored - contains downloaded audio)
│
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (gitignored)
└── .env.example          # Environment variables template
```

### Backend Architecture Layers

1. **API Layer** (`main.py`)
   - HTTP endpoints
   - Request/response handling
   - Error handling
   - CORS middleware

2. **Business Logic Layer** (`worker.py`)
   - Video processing orchestration
   - Background task management
   - Status tracking

3. **Service Layer** (`openai_client.py`, `youtube_downloader.py`, etc.)
   - External API integrations
   - Business logic for specific operations

4. **Data Layer** (`db/crud.py`, `db/models.py`)
   - Database operations
   - Data models
   - Query execution

---

## 🎨 Frontend Structure (`frontend/`)

```
frontend/
├── app/                  # Next.js App Router directory
│   ├── layout.tsx        # Root layout with Navbar
│   ├── page.tsx          # Home page (video submission)
│   ├── globals.css       # Global styles (dark theme)
│   ├── favicon.ico       # Site favicon
│   │
│   ├── history/          # History page route
│   │   └── page.tsx      # Video history listing
│   │
│   └── notes/            # Notes display route
│       └── [id]/         # Dynamic route for video ID
│           └── page.tsx  # Notes display page
│
├── components/           # Reusable React components
│   ├── Navbar.tsx        # Navigation bar component
│   ├── LanguageDropdown.tsx  # Language selection dropdown
│   ├── NotesViewer.tsx   # Markdown notes renderer
│   └── BootstrapClient.tsx   # Bootstrap JS loader
│
├── lib/                  # Frontend libraries and utilities
│   ├── languages.ts      # Language definitions (shared with backend)
│   └── db.ts             # Database types (if needed)
│
├── public/               # Static assets
│   └── *.svg             # SVG icons
│
├── package.json          # Node.js dependencies
├── tsconfig.json         # TypeScript configuration
├── next.config.js        # Next.js configuration
└── .env.local            # Environment variables (gitignored)
```

### Frontend Architecture Layers

1. **Pages Layer** (`app/`)
   - Route components
   - Page-level logic
   - Data fetching

2. **Components Layer** (`components/`)
   - Reusable UI components
   - Presentational components
   - Shared logic

3. **Utilities Layer** (`lib/`)
   - Helper functions
   - Type definitions
   - Shared constants

---

## 📊 Industry Standards Compliance

### ✅ Separation of Concerns
- Backend and frontend are completely separate
- Clear boundaries between API, business logic, and data layers
- Components are modular and reusable

### ✅ Type Safety
- TypeScript for frontend (type-safe JavaScript)
- Python type hints for backend
- Pydantic models for API validation

### ✅ Configuration Management
- Environment variables for configuration
- `.env.example` files for documentation
- No hardcoded secrets or URLs

### ✅ Dependency Management
- `requirements.txt` for Python dependencies
- `package.json` for Node.js dependencies
- Version pinning for stability

### ✅ Database Organization
- Separate models and CRUD operations
- Raw SQL for performance (asyncpg)
- SQLAlchemy models for reference

### ✅ Error Handling
- Consistent error response format
- Global exception handlers
- User-friendly error messages

### ✅ Documentation
- Comprehensive README.md
- Code comments and docstrings
- API documentation (Swagger UI)

---

## 🔄 Data Flow

```
User Input (Frontend)
    ↓
API Request (HTTP)
    ↓
FastAPI Endpoint (main.py)
    ↓
Background Task (worker.py)
    ↓
Service Layer (openai_client.py, youtube_downloader.py)
    ↓
Database (crud.py)
    ↓
Response (JSON)
    ↓
Frontend Display
```

---

## 📝 File Naming Conventions

### Backend (Python)
- **snake_case** for files and functions
- **PascalCase** for classes
- Descriptive names: `video_chunker.py`, `openai_client.py`

### Frontend (TypeScript/React)
- **PascalCase** for components: `Navbar.tsx`, `NotesViewer.tsx`
- **camelCase** for functions and variables
- **kebab-case** for routes: `notes/[id]/page.tsx`

---

## 🚀 Best Practices Followed

1. **Modular Design**: Each module has a single responsibility
2. **Async/Await**: Non-blocking I/O operations throughout
3. **Error Handling**: Comprehensive try-catch blocks
4. **Type Safety**: TypeScript and Python type hints
5. **Code Comments**: Detailed docstrings and inline comments
6. **Environment Config**: All config via environment variables
7. **Security**: Parameterized queries, input validation
8. **Performance**: Connection pooling, parallel processing
9. **Scalability**: Background tasks, async operations
10. **Maintainability**: Clear structure, comprehensive documentation

---

## 📦 Dependencies Organization

### Backend Dependencies (`requirements.txt`)
- **Web Framework**: FastAPI, Uvicorn
- **Database**: asyncpg, SQLAlchemy
- **AI/ML**: openai, openai-agents
- **Video Processing**: yt-dlp
- **Utilities**: python-dotenv, pydantic

### Frontend Dependencies (`package.json`)
- **Framework**: Next.js, React
- **Styling**: Bootstrap, Bootstrap Icons
- **Type Safety**: TypeScript
- **Build Tools**: ESLint, PostCSS

---

## 🔐 Security Considerations

1. **Environment Variables**: All secrets in `.env` (gitignored)
2. **SQL Injection Prevention**: Parameterized queries
3. **Input Validation**: Pydantic schemas for all requests
4. **CORS Configuration**: Configured for development (change in production)
5. **Error Messages**: Don't expose sensitive information

---

## 📈 Scalability Considerations

1. **Connection Pooling**: Database pool for efficient connections
2. **Background Tasks**: Non-blocking processing
3. **Caching**: Translation caching in database
4. **Parallel Processing**: Concurrent transcription of chunks
5. **File Cleanup**: Automatic cleanup of temporary files

---

This structure follows industry best practices and is ready for production deployment.

