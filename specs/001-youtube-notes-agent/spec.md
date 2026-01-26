# Feature Specification: YouTube Notes AI Agent

**Feature Branch**: `001-youtube-notes-agent`  
**Created**: 2025-01-27  
**Status**: Draft  
**Input**: User description: "Detailed deliverables and implementation guide. This document contains: file tree, environment variables, install & run commands, DB schema, Prisma + SQLAlchemy schemas, code snippets for key files (Next.js, FastAPI), prompts, security notes, UI behavior, and testing steps."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Process YouTube Video and Generate Notes (Priority: P1)

A user wants to quickly extract structured study notes from a YouTube video without manually watching and taking notes. They paste a YouTube URL into the system, and within a reasonable time, receive comprehensive, well-organized notes that capture the key information from the video.

**Why this priority**: This is the core value proposition of the system. Without the ability to process videos and generate notes, no other features matter. This story delivers the primary user benefit independently.

**Independent Test**: Can be fully tested by submitting a YouTube URL, waiting for processing to complete, and verifying that structured notes are generated and stored. The test delivers value even if no other features exist - users can process videos and access notes via direct database queries or API calls.

**Acceptance Scenarios**:

1. **Given** a user has a valid YouTube video URL, **When** they submit it for processing, **Then** the system processes the video and generates structured notes containing main heading, subheadings, bullet points, key insights, important quotes, summary, and actionable takeaways
2. **Given** a user submits an invalid or inaccessible YouTube URL, **When** processing is attempted, **Then** the system returns a clear error message explaining the issue
3. **Given** a user submits a very long video (over 2 hours), **When** processing completes, **Then** the system generates notes that capture the essential content despite the length
4. **Given** processing is in progress, **When** a user checks the status, **Then** they receive feedback indicating the current stage (downloading, transcribing, generating notes)

---

### User Story 2 - View Generated Notes (Priority: P2)

A user wants to read the structured notes that were generated from a processed video. They should be able to view the notes in a clear, readable format that preserves the structure (headings, bullet points, quotes, etc.) and includes the full transcript for reference.

**Why this priority**: Once notes are generated, users need to access and read them. This story enables users to consume the value created in Story 1. It can be tested independently by directly accessing stored notes.

**Independent Test**: Can be fully tested by retrieving a previously processed video's notes and displaying them in a readable format. The test delivers value independently - users can view notes even if they can't process new videos in the same session.

**Acceptance Scenarios**:

1. **Given** a video has been processed and notes are available, **When** a user requests to view the notes, **Then** they see the structured notes with main heading, subheadings, bullet points, key insights, important quotes, summary, and actionable takeaways clearly displayed
2. **Given** notes contain code blocks or technical content, **When** a user views the notes, **Then** code blocks are properly formatted and preserved
3. **Given** a user wants to see the original transcript, **When** they request it, **Then** the full transcript is accessible (either displayed or available in a collapsible section)
4. **Given** notes include timestamps for quotes, **When** a user views the notes, **Then** timestamps are displayed alongside the quotes

---

### User Story 3 - Translate Notes to Different Languages (Priority: P3)

A user wants to read the generated notes in their preferred language. They select a target language from a list of available languages, and the system translates the notes while preserving the structure and formatting.

**Why this priority**: Translation expands accessibility and user base, but the core value (processing and viewing notes) is already delivered in Stories 1 and 2. This story adds significant value for international users but is not required for the MVP.

**Independent Test**: Can be fully tested by selecting a language for existing notes and verifying that translated notes are generated and displayed with preserved structure. The test delivers value independently - users can translate any existing notes even if they can't process new videos.

**Acceptance Scenarios**:

1. **Given** notes exist for a video, **When** a user selects a target language from the available options, **Then** the system generates and displays translated notes that preserve the original structure (headings, bullet points, formatting)
2. **Given** notes contain code blocks or technical terms, **When** translation is performed, **Then** code blocks remain unchanged and technical terms are handled appropriately (either translated or kept in English based on context)
3. **Given** a user requests translation to a language, **When** a translation already exists for that language, **Then** the system displays the existing translation without regenerating
4. **Given** notes are being translated, **When** the process completes, **Then** the translated notes are stored for future access

---

### User Story 4 - View Processing History (Priority: P4)

A user wants to see a list of all videos they have processed previously, so they can easily access notes from past videos without needing to remember URLs or reprocess content.

**Why this priority**: History improves user experience and efficiency, but the core functionality (process, view, translate) works without it. Users can still access notes if they know the video identifier, making this a nice-to-have enhancement.

**Independent Test**: Can be fully tested by displaying a list of previously processed videos with metadata (title, date, thumbnail) and allowing navigation to view notes. The test delivers value independently - users can browse and access past notes even if they can't process new videos in the same session.

**Acceptance Scenarios**:

1. **Given** multiple videos have been processed, **When** a user views their history, **Then** they see a list of all processed videos with title, processing date, and thumbnail (if available)
2. **Given** a user wants to access notes from a past video, **When** they select a video from history, **Then** they are taken to the notes view for that video
3. **Given** history contains many videos, **When** a user views history, **Then** videos are displayed in a paginated or scrollable list with most recent first
4. **Given** a user wants to remove a video from history, **When** they delete it, **Then** the video and all associated translations are removed from the system

---

### Edge Cases

- What happens when a YouTube video is private, age-restricted, or region-locked?
- How does the system handle videos that are deleted or made unavailable after processing?
- What happens when a video has no speech or audio (music-only, silent video)?
- How does the system handle very short videos (under 1 minute) or very long videos (over 4 hours)?
- What happens when translation fails for a specific language?
- How does the system handle videos with multiple languages in the transcript?
- What happens when network connectivity is lost during processing?
- How does the system handle duplicate video submissions (same URL processed twice)?
- What happens when a video URL is malformed or points to a non-YouTube domain?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept YouTube video URLs as input for processing
- **FR-002**: System MUST download audio from YouTube videos for processing
- **FR-003**: System MUST transcribe audio content from videos into text
- **FR-004**: System MUST generate structured notes from transcripts containing: main heading, subheadings, bullet points, key insights section, important quotes section, final summary, and actionable takeaways
- **FR-005**: System MUST store processed videos with metadata including URL, title, transcript, generated notes, duration, thumbnail, and processing timestamp
- **FR-006**: System MUST provide a way for users to view generated notes in a readable, structured format
- **FR-007**: System MUST preserve Markdown formatting (headings, bullet points, code blocks) in generated notes
- **FR-008**: System MUST support translation of notes into 50+ languages
- **FR-009**: System MUST preserve note structure (headings, bullets, formatting) during translation
- **FR-010**: System MUST store translations linked to their source video
- **FR-011**: System MUST provide a history view showing all previously processed videos
- **FR-012**: System MUST display video metadata (title, date, thumbnail) in history view
- **FR-013**: System MUST allow users to access notes from history
- **FR-014**: System MUST handle processing errors gracefully and provide clear error messages to users
- **FR-015**: System MUST provide status feedback during video processing (downloading, transcribing, generating notes)
- **FR-016**: System MUST allow users to export notes in a printable or downloadable format
- **FR-017**: System MUST retain the full original transcript for reference alongside generated notes
- **FR-018**: System MUST handle code blocks and technical content appropriately in both notes and translations

### Key Entities *(include if feature involves data)*

- **Video**: Represents a processed YouTube video. Contains: unique identifier, YouTube URL, video title, full transcript text, generated structured notes, video duration in seconds, thumbnail image URL, and creation timestamp. Videos can have multiple translations.

- **Translation**: Represents a translated version of notes for a specific language. Contains: unique identifier, reference to source video, target language code, translated notes text preserving structure, and creation timestamp. Each translation belongs to exactly one video, and a video can have translations in multiple languages.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully process a YouTube video and receive structured notes within 5 minutes for videos up to 1 hour in length
- **SC-002**: Generated notes contain all required sections (heading, subheadings, bullets, insights, quotes, summary, takeaways) for 95% of successfully processed videos
- **SC-003**: Users can view generated notes in a readable format with preserved structure (headings, bullets, formatting) 100% of the time
- **SC-004**: Translation functionality supports at least 50 languages and successfully preserves note structure in 98% of translation requests
- **SC-005**: Users can access their processing history and view notes from any previously processed video within 2 seconds of request
- **SC-006**: System successfully processes and generates notes for 90% of valid, accessible YouTube video URLs submitted
- **SC-007**: Users receive clear error messages for failed processing attempts (invalid URLs, inaccessible videos, processing errors) 100% of the time
- **SC-008**: Notes export functionality allows users to generate a printable/downloadable version of notes in under 3 seconds
