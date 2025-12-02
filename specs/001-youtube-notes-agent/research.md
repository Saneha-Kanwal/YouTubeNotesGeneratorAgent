# Research & Technical Decisions

**Feature**: YouTube Notes AI Agent  
**Date**: 2025-01-27  
**Status**: Complete

## Overview

This document consolidates research findings and technical decisions for the YouTube Notes AI Agent implementation. All technical choices align with the project constitution and feature requirements.

## Technology Stack Decisions

### Backend Framework: FastAPI

**Decision**: Use FastAPI (Python) for backend API

**Rationale**: 
- FastAPI provides high performance with async/await support, essential for I/O-bound operations (YouTube downloads, OpenAI API calls)
- Automatic OpenAPI documentation generation
- Built-in data validation with Pydantic
- Excellent support for background tasks and long-running operations
- Constitution requirement (Principle 2)

**Alternatives Considered**:
- Django: Too heavy, synchronous by default, slower for async operations
- Flask: Lacks built-in async support, requires additional setup
- Express.js (Node.js): Would require different language, Python ecosystem better for yt-dlp and OpenAI integration

### Frontend Framework: Next.js 15 (App Router)

**Decision**: Use Next.js 15 with App Router

**Rationale**:
- Modern React patterns with Server Components
- Built-in API routes for proxying to FastAPI (optional)
- Excellent TypeScript support
- Constitution requirement (Principle 1)
- Optimal performance with automatic code splitting

**Alternatives Considered**:
- React (CRA/Vite): Would require additional routing and API setup
- Remix: Less mature ecosystem, smaller community
- SvelteKit: Different paradigm, team familiarity with React

### Database: PostgreSQL

**Decision**: Use PostgreSQL 15+

**Rationale**:
- Robust relational database with excellent text search capabilities
- UUID support for primary keys
- JSON/JSONB support for flexible metadata storage
- Constitution requirement (Principle 3)
- Industry standard for production applications

**Alternatives Considered**:
- MySQL: Less advanced JSON support, weaker UUID handling
- SQLite: Not suitable for production, lacks concurrent write performance
- MongoDB: NoSQL not needed for structured relational data

### YouTube Download: yt-dlp

**Decision**: Use yt-dlp for audio extraction

**Rationale**:
- Most actively maintained YouTube downloader
- Supports audio-only extraction (mp3, m4a formats)
- Handles various YouTube URL formats and edge cases
- Constitution requirement (Principle 4)
- Python library, integrates seamlessly with FastAPI

**Alternatives Considered**:
- youtube-dl: Less actively maintained, yt-dlp is a fork with better updates
- pytube: Less reliable, frequent breaking changes with YouTube updates
- Custom solution: Too complex, reinventing the wheel

### OpenAI Integration: Agent SDK

**Decision**: Use OpenAI Agent SDK syntax exclusively

**Rationale**:
- Constitution requirement (Principle 5) - MUST use Agent SDK, no chat completion, no swarm syntax
- Structured approach to AI interactions
- Better maintainability and consistency
- Supports both Whisper (transcription) and GPT (note generation, translation)

**Alternatives Considered**:
- Chat Completion API: Violates constitution (explicitly forbidden)
- Swarm syntax: Violates constitution (explicitly forbidden)
- Direct REST calls: Less structured, harder to maintain

### Database Access: Raw SQL Queries

**Decision**: Use raw SQL queries instead of ORM

**Rationale**:
- Explicit requirement from user: "must use raw queries, not use ORM"
- Full control over query performance
- Direct SQL execution for complex operations
- Prisma schema and SQLAlchemy models maintained for type safety reference only

**Implementation Approach**:
- Frontend: Use Prisma Client for connection management, but execute raw queries via `prisma.$queryRaw`
- Backend: Use SQLAlchemy engine for connection, but execute raw queries via `connection.execute(text(...))`
- Maintain schema files for type generation and documentation

**Alternatives Considered**:
- Full ORM usage: Violates explicit requirement
- Query builders: Still abstraction layer, raw SQL preferred

## Architecture Decisions

### Processing Flow

**Decision**: Asynchronous background processing with status polling

**Rationale**:
- Video processing is long-running (download, transcribe, generate notes)
- Prevents HTTP timeouts
- Allows user to check status without blocking
- Better user experience with progress feedback

**Flow**:
1. User submits YouTube URL → FastAPI endpoint
2. FastAPI validates URL, enqueues background task
3. Returns video_id immediately
4. Background task: download → transcribe → generate notes → store
5. Frontend polls status endpoint or uses WebSocket (future enhancement)

**Alternatives Considered**:
- Synchronous processing: Would cause HTTP timeouts for long videos
- Queue system (Celery/Redis): Adds complexity, not needed for MVP

### Translation Strategy

**Decision**: On-demand translation with caching

**Rationale**:
- Translations are expensive (OpenAI API calls)
- Store translations in database to avoid regeneration
- User selects language → check if exists → generate if missing → display

**Alternatives Considered**:
- Pre-translate all languages: Too expensive, most translations unused
- No caching: Wastes API calls, slower user experience

### Note Structure Format

**Decision**: Markdown format with specific sections

**Rationale**:
- Constitution requirement (Principle 7)
- Preserves structure during translation
- Easy to render in frontend
- Supports code blocks and formatting

**Required Sections**:
- Main heading (H1)
- TL;DR summary (one sentence)
- Major headings (H2)
- Subheadings (H3)
- Bullet lists
- Key Insights (numbered bullets)
- Important Quotes (with timestamps if available)
- Actionable Takeaways (5 practical actions)
- Full Transcript (collapsible/details block)

## Performance Considerations

### Video Length Handling

**Decision**: Support videos up to 4 hours, process in chunks if needed

**Rationale**:
- Success criteria requires handling videos up to 1 hour within 5 minutes
- Longer videos may need chunked processing
- Whisper API has token limits, may need to split transcript

**Implementation Notes**:
- Monitor processing time vs video length
- Consider chunking for videos > 2 hours
- Store processing metadata for optimization

### Concurrent Processing

**Decision**: Support multiple concurrent video processing requests

**Rationale**:
- Users may submit multiple videos
- Background tasks allow parallel processing
- FastAPI async support enables concurrency

**Limitations**:
- OpenAI API rate limits
- Server resource constraints (CPU, memory, disk)
- May need rate limiting or queue management for production

## Security Considerations

### API Key Management

**Decision**: Store OpenAI API key in environment variables, use Docker secrets in production

**Rationale**:
- Never commit secrets to version control
- Environment variables are standard practice
- Docker secrets provide additional security layer

### Input Validation

**Decision**: Validate YouTube URLs server-side before processing

**Rationale**:
- Prevent malicious URL submissions
- Validate URL format and domain
- Check video accessibility before processing

### Error Handling

**Decision**: Graceful error handling with user-friendly messages

**Rationale**:
- Constitution requirement (FR-014)
- Don't expose internal errors to users
- Log detailed errors server-side for debugging

## Testing Strategy

### Backend Testing

**Decision**: Use pytest with pytest-asyncio for FastAPI testing

**Rationale**:
- Standard Python testing framework
- Excellent async support
- Good integration with FastAPI TestClient

### Frontend Testing

**Decision**: Use Jest and React Testing Library

**Rationale**:
- Standard React testing tools
- Component testing with React Testing Library
- E2E testing with Playwright (optional, for critical flows)

## Deployment Considerations

### Containerization

**Decision**: Use Docker and docker-compose for local development and deployment

**Rationale**:
- Consistent environment across development and production
- Easy dependency management
- Isolated services (frontend, backend, database)

### Environment Configuration

**Decision**: Use .env files for configuration, .env.example for documentation

**Rationale**:
- Standard practice for configuration management
- Easy to override for different environments
- .env.example documents required variables

## Open Questions Resolved

All technical decisions have been made. No outstanding clarifications.

## Next Steps

1. Implement data model based on entities (Video, Translation)
2. Design API contracts for all endpoints
3. Create quickstart guide for setup and running
4. Begin implementation following task breakdown

