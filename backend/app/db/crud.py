"""
Database CRUD operations using raw SQL queries with asyncpg.
No ORM usage - all queries are raw SQL as per requirements.
"""
import asyncpg
from typing import Optional, List, Dict, Any
from uuid import UUID
import os


async def get_db_pool() -> asyncpg.Pool:
    """Create and return database connection pool."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")
    
    return await asyncpg.create_pool(database_url, min_size=2, max_size=10)


async def insert_video(pool: asyncpg.Pool, youtube_url: str) -> UUID:
    """Insert a new video record and return the video_id."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO videos (youtube_url)
            VALUES ($1)
            RETURNING id
            """,
            youtube_url
        )
        return row["id"]


async def update_video(
    pool: asyncpg.Pool,
    video_id: UUID,
    title: Optional[str] = None,
    transcript: Optional[str] = None,
    original_notes: Optional[str] = None,
    duration_seconds: Optional[int] = None,
    thumbnail_url: Optional[str] = None,
) -> None:
    """Update video record with processing results."""
    updates = []
    values = []
    param_num = 1

    if title is not None:
        updates.append(f"title = ${param_num}")
        values.append(title)
        param_num += 1
    if transcript is not None:
        updates.append(f"transcript = ${param_num}")
        values.append(transcript)
        param_num += 1
    if original_notes is not None:
        updates.append(f"original_notes = ${param_num}")
        values.append(original_notes)
        param_num += 1
    if duration_seconds is not None:
        updates.append(f"duration_seconds = ${param_num}")
        values.append(duration_seconds)
        param_num += 1
    if thumbnail_url is not None:
        updates.append(f"thumbnail_url = ${param_num}")
        values.append(thumbnail_url)
        param_num += 1

    if not updates:
        return

    values.append(video_id)
    query = f"""
        UPDATE videos
        SET {', '.join(updates)}
        WHERE id = ${param_num}
    """

    async with pool.acquire() as conn:
        await conn.execute(query, *values)


async def get_video_by_id(pool: asyncpg.Pool, video_id: UUID) -> Optional[Dict[str, Any]]:
    """Get video by ID with all fields."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, youtube_url, title, transcript, original_notes,
                   duration_seconds, thumbnail_url, created_at
            FROM videos
            WHERE id = $1
            """,
            video_id
        )
        if row:
            return dict(row)
        return None


async def get_video_by_url(pool: asyncpg.Pool, youtube_url: str) -> Optional[Dict[str, Any]]:
    """Get video by YouTube URL."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, youtube_url, title, transcript, original_notes,
                   duration_seconds, thumbnail_url, created_at
            FROM videos
            WHERE youtube_url = $1
            """,
            youtube_url
        )
        if row:
            return dict(row)
        return None


async def list_videos(
    pool: asyncpg.Pool,
    page: int = 1,
    limit: int = 20
) -> tuple[List[Dict[str, Any]], int]:
    """List all videos with pagination."""
    offset = (page - 1) * limit
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, youtube_url, title, duration_seconds, thumbnail_url, created_at
            FROM videos
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit, offset
        )
        total_row = await conn.fetchrow("SELECT COUNT(*) as count FROM videos")
        total = total_row["count"] if total_row else 0
        
        return [dict(row) for row in rows], total


async def delete_video(pool: asyncpg.Pool, video_id: UUID) -> bool:
    """Delete video by ID (translations cascade automatically)."""
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM videos WHERE id = $1",
            video_id
        )
        return result == "DELETE 1"


async def insert_translation(
    pool: asyncpg.Pool,
    video_id: UUID,
    target_lang: str,
    translated_notes: str
) -> UUID:
    """Insert a new translation record and return the translation_id."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO translations (video_id, target_lang, translated_notes)
            VALUES ($1, $2, $3)
            RETURNING id
            """,
            video_id, target_lang, translated_notes
        )
        return row["id"]


async def get_translation(
    pool: asyncpg.Pool,
    video_id: UUID,
    target_lang: str
) -> Optional[Dict[str, Any]]:
    """Get translation by video_id and target_lang."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT id, video_id, target_lang, translated_notes, created_at
            FROM translations
            WHERE video_id = $1 AND target_lang = $2
            """,
            video_id, target_lang
        )
        if row:
            return dict(row)
        return None


async def translation_exists(
    pool: asyncpg.Pool,
    video_id: UUID,
    target_lang: str
) -> bool:
    """Check if translation exists for video_id and target_lang."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT EXISTS(SELECT 1 FROM translations WHERE video_id = $1 AND target_lang = $2)
            """,
            video_id, target_lang
        )
        return row["exists"] if row else False


async def list_translations(
    pool: asyncpg.Pool,
    video_id: UUID
) -> List[Dict[str, Any]]:
    """List all translations for a video."""
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT id, target_lang, created_at
            FROM translations
            WHERE video_id = $1
            ORDER BY target_lang
            """,
            video_id
        )
        return [dict(row) for row in rows]

