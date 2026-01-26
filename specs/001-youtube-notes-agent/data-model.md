# Data Model

**Feature**: YouTube Notes AI Agent  
**Date**: 2025-01-27  
**Status**: Complete

## Overview

This document defines the data model for the YouTube Notes AI Agent. The model consists of two main entities: `Video` and `Translation`. All data is stored in PostgreSQL using raw SQL queries (no ORM usage per requirements).

## Entities

### Video

Represents a processed YouTube video with its metadata, transcript, and generated notes.

**Table Name**: `videos`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the video record |
| `youtube_url` | TEXT | NOT NULL, UNIQUE | Original YouTube video URL |
| `title` | TEXT | NULL | Video title extracted from YouTube |
| `transcript` | TEXT | NULL | Full transcript text from Whisper transcription |
| `original_notes` | TEXT | NULL | Generated structured notes in Markdown format |
| `duration_seconds` | INTEGER | NULL | Video duration in seconds |
| `thumbnail_url` | TEXT | NULL | YouTube thumbnail image URL |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | Timestamp when video was processed |

**Relationships**:
- One-to-many with `Translation` (one video can have many translations)

**Validation Rules**:
- `youtube_url` must be a valid YouTube URL format
- `youtube_url` must be unique (prevent duplicate processing)
- `original_notes` must be valid Markdown when present
- `duration_seconds` must be positive when present
- `created_at` is automatically set on insert

**State Transitions**:
- Initial: Video record created with `youtube_url`, `id`, `created_at`
- Processing: `title`, `transcript`, `original_notes`, `duration_seconds`, `thumbnail_url` populated as processing completes
- Complete: All fields populated (except nullable fields that may be unavailable)

**SQL Schema**:

```sql
CREATE TABLE videos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_url text NOT NULL UNIQUE,
  title text,
  transcript text,
  original_notes text,
  duration_seconds int,
  thumbnail_url text,
  created_at timestamptz DEFAULT now() NOT NULL
);

CREATE INDEX idx_videos_youtube_url ON videos(youtube_url);
CREATE INDEX idx_videos_created_at ON videos(created_at DESC);
```

### Translation

Represents a translated version of notes for a specific language.

**Table Name**: `translations`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the translation record |
| `video_id` | UUID | NOT NULL, FOREIGN KEY REFERENCES videos(id) ON DELETE CASCADE | Reference to the source video |
| `target_lang` | TEXT | NOT NULL | ISO 639-1 language code (e.g., 'es', 'fr', 'de') |
| `translated_notes` | TEXT | NOT NULL | Translated notes in Markdown format, preserving structure |
| `created_at` | TIMESTAMPTZ | DEFAULT now(), NOT NULL | Timestamp when translation was created |

**Relationships**:
- Many-to-one with `Video` (many translations belong to one video)
- Unique constraint on (`video_id`, `target_lang`) to prevent duplicate translations

**Validation Rules**:
- `target_lang` must be a valid ISO 639-1 language code (2 characters)
- `target_lang` must be one of the supported 50+ languages
- `translated_notes` must preserve Markdown structure from original notes
- `video_id` must reference an existing video
- Combination of `video_id` and `target_lang` must be unique

**State Transitions**:
- Initial: Translation record created with `video_id`, `target_lang`, `id`, `created_at`
- Complete: `translated_notes` populated with translated content

**SQL Schema**:

```sql
CREATE TABLE translations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id uuid NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  target_lang text NOT NULL,
  translated_notes text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  UNIQUE(video_id, target_lang)
);

CREATE INDEX idx_translations_video_id ON translations(video_id);
CREATE INDEX idx_translations_target_lang ON translations(target_lang);
CREATE INDEX idx_translations_video_lang ON translations(video_id, target_lang);
```

## Data Access Patterns

### Common Queries

**Get video by ID**:
```sql
SELECT * FROM videos WHERE id = $1;
```

**Get video by YouTube URL**:
```sql
SELECT * FROM videos WHERE youtube_url = $1;
```

**Get all videos (history)**:
```sql
SELECT * FROM videos ORDER BY created_at DESC;
```

**Get translations for a video**:
```sql
SELECT * FROM translations WHERE video_id = $1 ORDER BY target_lang;
```

**Get specific translation**:
```sql
SELECT * FROM translations WHERE video_id = $1 AND target_lang = $2;
```

**Check if translation exists**:
```sql
SELECT EXISTS(SELECT 1 FROM translations WHERE video_id = $1 AND target_lang = $2);
```

**Delete video and cascade translations**:
```sql
DELETE FROM videos WHERE id = $1;
-- Translations automatically deleted via CASCADE
```

## Notes on Raw SQL Usage

While we use raw SQL queries, we maintain:

1. **Prisma Schema** (frontend): For TypeScript type generation and connection management
2. **SQLAlchemy Models** (backend): For reference and connection management
3. **Raw SQL Execution**: All actual queries use raw SQL via:
   - Frontend: `prisma.$queryRaw` or `prisma.$executeRaw`
   - Backend: `connection.execute(text(...))` or `session.execute(text(...))`

This approach provides:
- Type safety through schema definitions
- Full control over query performance
- Direct SQL execution as required
- Documentation through schema files

## Supported Languages

The system supports 50+ languages for translation. Language codes follow ISO 639-1 standard (2-character codes). Examples:

- `en` - English (original)
- `es` - Spanish
- `fr` - French
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ko` - Korean
- `ar` - Arabic
- `pt` - Portuguese
- `ru` - Russian
- ... (50+ total)

Full list will be maintained in frontend constants and validated on backend.

## Data Migration Considerations

**Initial Migration**:
- Create `videos` table
- Create `translations` table
- Create indexes for performance

**Future Migrations**:
- May add columns for additional metadata (processing status, error messages, etc.)
- May add indexes for new query patterns
- May add constraints for data validation

All migrations will use Alembic (optional per constitution) or raw SQL migration scripts.

