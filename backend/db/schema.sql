-- YouTube Notes AI Agent Database Schema
-- Created: 2025-01-27

-- Videos table
CREATE TABLE IF NOT EXISTS videos (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  youtube_url text NOT NULL UNIQUE,
  title text,
  transcript text,
  original_notes text,
  duration_seconds int,
  thumbnail_url text,
  created_at timestamptz DEFAULT now() NOT NULL
);

-- Indexes for videos table
CREATE INDEX IF NOT EXISTS idx_videos_youtube_url ON videos(youtube_url);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at DESC);

-- Translations table
CREATE TABLE IF NOT EXISTS translations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id uuid NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  target_lang text NOT NULL,
  translated_notes text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  UNIQUE(video_id, target_lang)
);

-- Indexes for translations table
CREATE INDEX IF NOT EXISTS idx_translations_video_id ON translations(video_id);
CREATE INDEX IF NOT EXISTS idx_translations_target_lang ON translations(target_lang);
CREATE INDEX IF NOT EXISTS idx_translations_video_lang ON translations(video_id, target_lang);

