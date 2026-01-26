<!--
Sync Impact Report:
Version change: N/A → 1.0.0 (initial constitution)
Modified principles: N/A (initial creation)
Added sections: All sections (initial creation)
Removed sections: N/A
Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md (Constitution Check section populated with specific principles)
  - ✅ verified: .specify/templates/spec-template.md (no constitution-specific content, compatible as-is)
  - ✅ verified: .specify/templates/tasks-template.md (no constitution-specific content, compatible as-is)
  - ⚠ pending: .specify/templates/commands/*.md (command templates not yet created, will be verified when created)
Follow-up TODOs: None
-->

# Project Constitution

**Project Name:** YouTube Notes AI Agent  
**Constitution Version:** 1.0.0  
**Ratification Date:** 2025-01-27  
**Last Amended Date:** 2025-01-27

## Purpose

The YouTube Notes AI Agent is a production-grade application that processes YouTube videos to generate structured, comprehensive notes. The workflow is: paste a YouTube link → download audio → transcribe with Whisper → generate structured notes with GPT in text format → store notes with support for translation into 50+ languages, history tracking, and a user interface.

The generated notes include:
- Main heading
- Subheadings
- Bullet points
- Key insights
- Important quotes
- Final summary
- Actionable takeaways

## Principles

### Principle 1: Frontend Technology Stack

**MUST** use Next.js 15 with App Router for the frontend framework. **MUST** use Bootstrap for UI styling and component library. The frontend **MUST** provide a user interface for:
- YouTube link input
- Note viewing and history
- Translation interface (50+ languages)
- User interaction and navigation

**Rationale:** Next.js 15 App Router provides modern React patterns, server components, and optimal performance. Bootstrap ensures consistent, responsive UI without additional design overhead.

### Principle 2: Backend Technology Stack

**MUST** use FastAPI (Python) for the backend API. FastAPI **MUST** handle all heavy computational tasks including:
- YouTube audio download via yt-dlp (or youtube-dl)
- Audio transcription via Whisper API
- Structured note generation via GPT API calls
- Server execution via Uvicorn

**Rationale:** FastAPI provides high performance, automatic API documentation, and excellent async support for I/O-bound operations like API calls and file processing.

### Principle 3: Database and ORM Strategy

**MUST** use PostgreSQL for persistent storage of notes, user data, and history. **MUST** use Prisma on the frontend (Next.js) side for type-safe database access. **MUST** use SQLAlchemy on the backend (FastAPI) side for database models and migrations. Alembic is optional for migration management but recommended.

**Rationale:** PostgreSQL provides robust relational data storage. Prisma ensures type safety in TypeScript/Next.js. SQLAlchemy provides Python-native ORM with migration support via Alembic.

### Principle 4: YouTube Audio Download

**MUST** use yt-dlp (or youtube-dl as fallback) for downloading audio from YouTube videos. The download process **MUST** be handled server-side in the FastAPI backend.

**Rationale:** yt-dlp is the most reliable and actively maintained tool for YouTube content extraction, supporting various formats and quality options.

### Principle 5: OpenAI API Integration

**MUST** use OpenAI API for both Whisper transcription and GPT-based note generation. **MUST NOT** use chat completion endpoints or swarm syntax. **MUST** use only OpenAI Agent SDK syntax for all API interactions.

**Rationale:** OpenAI provides state-of-the-art transcription (Whisper) and text generation (GPT) capabilities. The Agent SDK provides a structured, maintainable approach to AI interactions.

### Principle 6: External API Constraints

**MUST NOT** use any other paid APIs beyond OpenAI. All external services **MUST** be free/open-source alternatives or the core OpenAI API.

**Rationale:** Minimizes operational costs and vendor lock-in while maintaining core functionality through OpenAI's comprehensive API offerings.

### Principle 7: Note Structure and Format

Generated notes **MUST** follow a structured text format including:
- Main heading
- Subheadings
- Bullet points
- Key insights
- Key quotes
- Final summary
- Actionable takeaways

**Rationale:** Structured format ensures consistency, readability, and enables programmatic processing and translation.

### Principle 8: Translation Support

**MUST** support translation of generated notes into 50+ languages. Translation **MUST** be accessible through the user interface and **MUST** be stored in the database for history tracking.

**Rationale:** Broad language support maximizes accessibility and user base across global markets.

### Principle 9: History and Persistence

**MUST** maintain a complete history of all processed videos and generated notes. History **MUST** be accessible through the UI and **MUST** be stored persistently in PostgreSQL.

**Rationale:** History enables users to review past notes, track changes, and access previously generated content without reprocessing.

## Governance

### Amendment Procedure

Constitution amendments **MUST** follow this process:
1. Propose amendment with clear rationale
2. Update version number according to semantic versioning
3. Update `LAST_AMENDED_DATE` to current date
4. Update Sync Impact Report in constitution header
5. Propagate changes to all dependent templates and documentation
6. Document amendment in commit message

### Versioning Policy

Version numbers follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR:** Backward incompatible governance/principle removals or redefinitions
- **MINOR:** New principle/section added or materially expanded guidance
- **PATCH:** Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

All code, architecture decisions, and feature implementations **MUST** be reviewed against this constitution. Any deviation **MUST** be:
1. Documented with explicit rationale
2. Proposed as a constitution amendment if the deviation becomes standard practice
3. Flagged in code reviews and architectural discussions

### Review Expectations

- Constitution compliance **MUST** be verified during:
  - Feature specification reviews
  - Architecture decisions
  - Technology stack selections
  - External dependency additions
  - API integration designs
