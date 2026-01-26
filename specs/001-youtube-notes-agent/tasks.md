# Tasks: YouTube Notes AI Agent

**Input**: Design documents from `/specs/001-youtube-notes-agent/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are not explicitly requested in the feature specification, so no test tasks are included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/`
- Paths follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure with backend/ and frontend/ directories at repository root
- [x] T002 [P] Initialize backend Python project with requirements.txt in backend/
- [x] T003 [P] Initialize frontend Next.js 15 project with package.json in frontend/
- [x] T004 [P] Create docker-compose.yml at repository root with PostgreSQL, backend, and frontend services
- [x] T005 [P] Create backend/.env.example with OPENAI_API_KEY, DATABASE_URL, YT_DLP_BINARY, FASTAPI_HOST, FASTAPI_PORT
- [x] T006 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_BASE
- [x] T007 [P] Create backend/Dockerfile for FastAPI application
- [x] T008 [P] Create README.md at repository root with project overview
- [x] T009 [P] Configure backend linting (ruff or black) in backend/pyproject.toml or backend/.ruff.toml
- [x] T010 [P] Configure frontend linting (ESLint) in frontend/.eslintrc.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create PostgreSQL database schema with videos and translations tables in backend/db/schema.sql (from data-model.md)
- [x] T012 [P] Create backend/app/db/models.py with SQLAlchemy models for Video and Translation (for reference only, raw SQL will be used)
- [x] T013 [P] Create backend/app/db/crud.py with raw SQL query functions using asyncpg connection
- [x] T014 [P] Create backend/app/schemas.py with Pydantic request/response schemas for all API endpoints
- [x] T015 [P] Create backend/app/utils.py with helper functions (URL validation, error formatting)
- [x] T016 Create backend/app/main.py with FastAPI app initialization, CORS configuration, and base route structure
- [x] T017 [P] Create frontend/prisma/schema.prisma with Video and Translation models (for type safety, raw queries will be used)
- [x] T018 [P] Create frontend/lib/db.ts with PostgreSQL connection setup using Prisma Client for raw queries
- [x] T019 [P] Create frontend/components/ directory structure
- [x] T020 Configure environment variable loading in backend/app/main.py using python-dotenv
- [x] T021 Setup database connection pool in backend/app/db/crud.py using asyncpg
- [x] T022 Create error handling middleware in backend/app/main.py for consistent error responses

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Process YouTube Video and Generate Notes (Priority: P1) 🎯 MVP

**Goal**: Users can submit a YouTube URL and receive structured notes after processing completes. The system downloads audio, transcribes with Whisper, generates notes with GPT, and stores results.

**Independent Test**: Submit a YouTube URL via POST /process-video, poll /videos/{id}/status until completed, then retrieve video with notes via GET /videos/{id}. Verify notes contain all required sections (heading, subheadings, bullets, insights, quotes, summary, takeaways).

### Implementation for User Story 1

- [x] T023 [P] [US1] Create backend/app/youtube_downloader.py with yt-dlp wrapper function to download audio and extract metadata (title, duration, thumbnail)
- [x] T024 [P] [US1] Create backend/app/openai_client.py with OpenAI Agent SDK wrapper functions for Whisper transcription and GPT note generation
- [x] T025 [US1] Create backend/app/worker.py with process_video_task function that orchestrates: download audio → transcribe → generate notes → store in database
- [x] T026 [US1] Implement POST /process-video endpoint in backend/app/main.py that validates URL, creates video record, and enqueues background task
- [x] T027 [US1] Implement GET /videos/{video_id}/status endpoint in backend/app/main.py to return processing status
- [x] T028 [US1] Add YouTube URL validation function in backend/app/utils.py to validate URL format and domain
- [x] T029 [US1] Implement note generation prompt in backend/app/openai_client.py following constitution requirements (main heading, subheadings, bullets, insights, quotes, summary, takeaways)
- [x] T030 [US1] Add raw SQL query in backend/app/db/crud.py to insert video record with youtube_url and return video_id
- [x] T031 [US1] Add raw SQL query in backend/app/db/crud.py to update video record with transcript, original_notes, title, duration_seconds, thumbnail_url
- [x] T032 [US1] Add error handling in backend/app/worker.py for download failures, transcription errors, and note generation errors
- [x] T033 [US1] Add audio file cleanup in backend/app/worker.py after processing completes
- [x] T034 [US1] Create frontend/app/page.tsx with YouTube URL input form and submit button
- [x] T034 [US1] Implement frontend API call to POST /process-video in frontend/app/page.tsx
- [x] T036 [US1] Add status polling logic in frontend/app/page.tsx to check /videos/{id}/status until completed
- [x] T037 [US1] Add loading spinner and status messages in frontend/app/page.tsx during processing

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can submit YouTube URLs, see processing status, and retrieve completed notes.

---

## Phase 4: User Story 2 - View Generated Notes (Priority: P2)

**Goal**: Users can view generated notes in a readable format with preserved Markdown structure, including transcript access.

**Independent Test**: Retrieve a processed video via GET /videos/{id} and display notes in a formatted view. Verify headings, bullets, code blocks, and transcript are all properly displayed.

### Implementation for User Story 2

- [x] T038 [US2] Implement GET /videos/{video_id} endpoint in backend/app/main.py to retrieve video with notes and transcript
- [x] T039 [US2] Add raw SQL query in backend/app/db/crud.py to select video by ID with all fields
- [x] T040 [US2] Create frontend/app/notes/[id]/page.tsx for note detail view
- [x] T041 [US2] Create frontend/components/NotesViewer.tsx component to render Markdown notes with proper formatting
- [x] T042 [US2] Add Markdown rendering library (react-markdown or marked) to frontend/package.json
- [x] T043 [US2] Implement code block syntax highlighting in frontend/components/NotesViewer.tsx
- [x] T044 [US2] Add collapsible transcript section in frontend/app/notes/[id]/page.tsx using Bootstrap collapse component
- [x] T045 [US2] Display video metadata (title, duration, thumbnail) in frontend/app/notes/[id]/page.tsx
- [x] T046 [US2] Add timestamp display for quotes in frontend/components/NotesViewer.tsx if timestamps exist in notes
- [x] T047 [US2] Implement frontend API call to GET /videos/{id} in frontend/app/notes/[id]/page.tsx
- [x] T048 [US2] Add error handling in frontend/app/notes/[id]/page.tsx for 404 and other errors
- [x] T049 [US2] Add navigation from home page to notes page after processing completes in frontend/app/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can process videos and view the generated notes with full formatting.

---

## Phase 5: User Story 3 - Translate Notes to Different Languages (Priority: P3)

**Goal**: Users can translate notes to 50+ languages with preserved Markdown structure. Translations are cached to avoid regeneration.

**Independent Test**: Select a language for existing notes, verify translation is generated/stored, and displayed with preserved structure. Verify code blocks remain unchanged.

### Implementation for User Story 3

- [x] T050 [US3] Add translation function in backend/app/openai_client.py using OpenAI Agent SDK to translate notes while preserving Markdown structure
- [x] T051 [US3] Add raw SQL query in backend/app/db/crud.py to check if translation exists for video_id and target_lang
- [x] T052 [US3] Add raw SQL query in backend/app/db/crud.py to insert translation record with video_id, target_lang, translated_notes
- [x] T053 [US3] Add raw SQL query in backend/app/db/crud.py to select translation by video_id and target_lang
- [x] T054 [US3] Implement POST /translate endpoint in backend/app/main.py that checks cache, generates if missing, and returns translation
- [x] T055 [US3] Add language validation in backend/app/utils.py to verify ISO 639-1 language codes (2 characters)
- [x] T056 [US3] Create frontend/lib/languages.ts with list of 50+ supported languages (ISO codes and display names)
- [x] T057 [US3] Create frontend/components/LanguageDropdown.tsx component with language selection dropdown
- [x] T058 [US3] Add language dropdown to frontend/app/notes/[id]/page.tsx
- [x] T059 [US3] Implement frontend API call to POST /translate in frontend/app/notes/[id]/page.tsx
- [x] T060 [US3] Add translation loading state in frontend/app/notes/[id]/page.tsx
- [x] T061 [US3] Update frontend/components/NotesViewer.tsx to display translated notes when language is selected
- [x] T062 [US3] Add "was_cached" indicator in frontend/app/notes/[id]/page.tsx to show if translation was retrieved from cache
- [x] T063 [US3] Implement GET /videos/{video_id}/translations endpoint in backend/app/main.py to list all available translations
- [x] T064 [US3] Add raw SQL query in backend/app/db/crud.py to select all translations for a video_id

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently. Users can process videos, view notes, and translate them to different languages.

---

## Phase 6: User Story 4 - View Processing History (Priority: P4)

**Goal**: Users can view a list of all processed videos with metadata and navigate to view notes. Users can delete videos from history.

**Independent Test**: Display list of all processed videos with title, date, thumbnail. Click video to navigate to notes. Delete video and verify it's removed.

### Implementation for User Story 4

- [x] T065 [US4] Implement GET /videos endpoint in backend/app/main.py with pagination support (page, limit parameters)
- [x] T066 [US4] Add raw SQL query in backend/app/db/crud.py to select all videos ordered by created_at DESC with pagination
- [x] T067 [US4] Add raw SQL query in backend/app/db/crud.py to count total videos for pagination
- [x] T068 [US4] Implement DELETE /videos/{video_id} endpoint in backend/app/main.py to delete video and cascade translations
- [x] T069 [US4] Add raw SQL query in backend/app/db/crud.py to delete video by ID (translations cascade automatically)
- [x] T070 [US4] Create frontend/app/history/page.tsx for history list view
- [x] T071 [US4] Implement frontend API call to GET /videos with pagination in frontend/app/history/page.tsx
- [x] T072 [US4] Display video list with title, thumbnail, duration, and created_at in frontend/app/history/page.tsx using Bootstrap cards
- [x] T073 [US4] Add pagination controls in frontend/app/history/page.tsx using Bootstrap pagination component
- [x] T074 [US4] Add navigation link from video card to notes page in frontend/app/history/page.tsx
- [x] T075 [US4] Add delete button for each video in frontend/app/history/page.tsx
- [x] T076 [US4] Implement frontend API call to DELETE /videos/{id} in frontend/app/history/page.tsx
- [x] T077 [US4] Add confirmation dialog before deletion in frontend/app/history/page.tsx
- [x] T078 [US4] Add navigation link to history page in frontend/app/page.tsx header/navigation
- [x] T079 [US4] Add navigation link to history page in frontend/app/notes/[id]/page.tsx

**Checkpoint**: At this point, all user stories should be independently functional. Users can process videos, view notes, translate them, and manage their history.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T080 [P] Add notes export functionality (PDF/print) in frontend/app/notes/[id]/page.tsx using window.print() or html2pdf library
- [ ] T081 [P] Add error boundary component in frontend/app/ for graceful error handling
- [ ] T082 [P] Add loading skeletons in frontend components for better UX during data fetching
- [ ] T083 [P] Add input validation feedback in frontend/app/page.tsx for YouTube URL format
- [ ] T084 [P] Improve error messages across all frontend pages with user-friendly messages
- [ ] T085 [P] Add logging for all backend operations in backend/app/worker.py and backend/app/main.py
- [ ] T086 [P] Add request/response logging middleware in backend/app/main.py
- [ ] T087 [P] Update README.md with setup instructions from quickstart.md
- [ ] T088 [P] Add environment variable validation on backend startup in backend/app/main.py
- [ ] T089 [P] Add health check endpoint GET /health in backend/app/main.py
- [ ] T090 [P] Add rate limiting for /process-video endpoint in backend/app/main.py to prevent abuse
- [ ] T091 [P] Add input sanitization for YouTube URLs in backend/app/utils.py
- [ ] T092 [P] Add Bootstrap styling improvements across all frontend pages for consistent UI
- [ ] T093 [P] Add responsive design improvements for mobile devices in frontend components
- [ ] T094 [P] Run quickstart.md validation to ensure all setup steps work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 for data (needs processed videos), but can be tested independently with existing data
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for data (needs notes to translate), but can be tested independently with existing notes
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on US1 for data (needs videos to list), but can be tested independently with existing videos

### Within Each User Story

- Database queries before services
- Services before endpoints
- Backend endpoints before frontend integration
- Core implementation before UI polish
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (if team capacity allows)
- Backend and frontend tasks within a story can often run in parallel after API contracts are defined
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch backend and frontend setup tasks in parallel:
Task: "Create backend/app/youtube_downloader.py"
Task: "Create backend/app/openai_client.py"
Task: "Create frontend/app/page.tsx"
Task: "Add YouTube URL validation function"

# After backend endpoints are ready, frontend integration can proceed:
Task: "Implement frontend API call to POST /process-video"
Task: "Add status polling logic"
Task: "Add loading spinner and status messages"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Submit YouTube URL
   - Verify processing completes
   - Verify notes are generated with all required sections
   - Verify notes are stored in database
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (backend focus)
   - Developer B: User Story 1 (frontend focus)
   - Developer C: User Story 2 (can start after US1 backend is ready)
3. After US1 completes:
   - Developer A: User Story 3 (translation backend)
   - Developer B: User Story 2 (view notes frontend)
   - Developer C: User Story 4 (history)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All database operations use raw SQL queries (no ORM)
- All OpenAI interactions use Agent SDK syntax (no chat completion, no swarm syntax)
- Frontend uses Bootstrap for styling (constitution requirement)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

