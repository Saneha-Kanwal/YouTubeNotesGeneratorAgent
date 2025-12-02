# Implementation Plan: YouTube Notes AI Agent

**Branch**: `001-youtube-notes-agent` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-youtube-notes-agent/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a production-grade YouTube Notes AI Agent that processes YouTube videos to generate structured study notes. Users submit YouTube URLs, and the system downloads audio, transcribes with Whisper, generates structured notes with GPT, and stores results with translation support. The system consists of a Next.js 15 frontend (App Router + Bootstrap) and a FastAPI backend (Python) with PostgreSQL storage. Notes include main headings, subheadings, bullet points, key insights, quotes, summaries, and actionable takeaways. Translation support for 50+ languages and full history tracking are included.

## Technical Context

**Language/Version**: 
- Backend: Python 3.11+
- Frontend: TypeScript 5.x with Next.js 15

**Primary Dependencies**: 
- Backend: FastAPI, uvicorn, openai (Agent SDK), yt-dlp, sqlalchemy, asyncpg, pydantic, alembic
- Frontend: Next.js 15 (App Router), React 19, Bootstrap 5, Prisma Client, TypeScript

**Storage**: PostgreSQL 15+ (persistent storage for videos, transcripts, notes, translations)

**Testing**: 
- Backend: pytest, pytest-asyncio, httpx (for FastAPI testing)
- Frontend: Jest, React Testing Library, Playwright (optional E2E)

**Target Platform**: 
- Backend: Linux server (containerized with Docker)
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge)

**Project Type**: Web application (frontend + backend)

**Performance Goals**: 
- Process videos up to 1 hour in length within 5 minutes (SC-001)
- View notes within 2 seconds (SC-005)
- Export notes in under 3 seconds (SC-008)
- Support concurrent processing of multiple videos

**Constraints**: 
- Must use raw SQL queries (no ORM usage per requirements)
- Must use OpenAI Agent SDK syntax only (no chat completion, no swarm syntax)
- Must support 50+ languages for translation
- Must handle videos up to 4 hours in length
- Must preserve Markdown structure during translation
- No other paid APIs beyond OpenAI

**Scale/Scope**: 
- Initial: Single-user or small team usage
- Videos: Hundreds to thousands of processed videos
- Translations: 50+ languages per video
- Storage: Transcripts and notes (text data, relatively small)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Verification

Verify compliance with `.specify/memory/constitution.md`:

- [x] **Frontend**: Uses Next.js 15 (App Router) + Bootstrap only
- [x] **Backend**: Uses FastAPI (Python) for heavy tasks, Uvicorn for server
- [x] **Database**: Uses PostgreSQL with Prisma (frontend) and SQLAlchemy (backend)
- [x] **YouTube Download**: Uses yt-dlp (or youtube-dl) for audio extraction
- [x] **OpenAI Integration**: Uses OpenAI Agent SDK syntax only (no chat completion, no swarm syntax)
- [x] **External APIs**: No other paid APIs beyond OpenAI
- [x] **Note Structure**: Follows required format (main heading, subheadings, bullet points, key insights, quotes, summary, takeaways)
- [x] **Translation**: Supports 50+ languages if feature involves note display
- [x] **History**: Persistent storage in PostgreSQL if feature involves data storage

**Pre-Phase 0 Status**: ✅ All checks passed

### Post-Phase 1 Verification

After completing design phase, all constitution principles remain satisfied:

- [x] **Frontend**: Next.js 15 (App Router) + Bootstrap confirmed in project structure
- [x] **Backend**: FastAPI with Uvicorn confirmed in technical context
- [x] **Database**: PostgreSQL with Prisma (frontend) and SQLAlchemy (backend) confirmed, raw SQL queries used as required
- [x] **YouTube Download**: yt-dlp confirmed in dependencies and research
- [x] **OpenAI Integration**: OpenAI Agent SDK syntax confirmed in research and requirements
- [x] **External APIs**: Only OpenAI API used, confirmed in research
- [x] **Note Structure**: Required format documented in data model and API contracts
- [x] **Translation**: 50+ languages supported, documented in data model
- [x] **History**: PostgreSQL storage confirmed in data model

**Post-Phase 1 Status**: ✅ All checks passed, no violations

**Violations**: None. All constitution principles are satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py                      # FastAPI app, routes
│   ├── worker.py                    # orchestration + helper functions
│   ├── youtube_downloader.py        # yt-dlp wrapper
│   ├── openai_client.py             # OpenAI wrapper (Whisper, GPT, translate)
│   ├── db/
│   │   ├── models.py                # SQLAlchemy models (for reference, but use raw queries)
│   │   └── crud.py                  # CRUD helpers (raw SQL)
│   ├── schemas.py                   # pydantic request/response schemas
│   └── utils.py                     # helpers
├── requirements.txt
├── Dockerfile
└── .env.example

frontend/
├── app/
│   ├── page.tsx                     # Home page
│   ├── notes/[id]/page.tsx          # Note detail + translate
│   └── history/page.tsx             # History page
├── components/
│   ├── NotesViewer.tsx
│   └── LanguageDropdown.tsx
├── prisma/
│   └── schema.prisma                # Prisma schema (for type safety, but use raw queries)
├── lib/
│   └── db.ts                        # Database connection (raw queries)
├── package.json
├── tailwind.config.js
└── .env.local.example

docker-compose.yml
README.md
.env.example
```

**Structure Decision**: Web application structure with separate frontend and backend directories. Backend uses FastAPI with Python, frontend uses Next.js 15 with TypeScript. Both use raw SQL queries (no ORM usage) but maintain type safety through Prisma schema (frontend) and SQLAlchemy models (backend) for reference only.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution principles are satisfied.
