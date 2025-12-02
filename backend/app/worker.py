"""
Background worker for processing videos.
Orchestrates: download audio → transcribe → generate notes → store in database.
Optimized for speed with parallel processing.
"""
import os
import asyncio
from uuid import UUID
import asyncpg
from app.db.crud import get_db_pool, update_video
from app.youtube_downloader import download_audio
from app.openai_client import transcribe_audio, generate_notes

# Global processing status tracking (in production, use Redis or database)
processing_status: dict[str, dict] = {}


async def process_video_task(video_id: str, youtube_url: str):
    """
    Process a YouTube video: download, transcribe, generate notes, store.
    Optimized with parallel transcription for faster processing.
    
    Updates processing status throughout the process.
    """
    db_pool = await get_db_pool()
    audio_path = None
    
    try:
        # Update status: downloading
        processing_status[video_id] = {
            "status": "downloading",
            "progress": "Downloading audio from YouTube...",
            "error": None,
        }
        
        # Step 1: Download audio (with automatic chunking for long videos)
        from app.video_chunker import download_video_in_chunks
        
        # Check if video should be chunked (> 30 minutes)
        audio_paths, metadata = await download_video_in_chunks(youtube_url, chunk_duration_minutes=12.0)
        
        # Update status: transcribing
        if len(audio_paths) > 1:
            processing_status[video_id] = {
                "status": "transcribing",
                "progress": f"Transcribing {len(audio_paths)} video chunks in parallel for faster processing...",
                "error": None,
            }
        else:
            file_size_mb = os.path.getsize(audio_paths[0]) / (1024 * 1024) if os.path.exists(audio_paths[0]) else 0
            if file_size_mb > 25:
                processing_status[video_id] = {
                    "status": "transcribing",
                    "progress": f"Transcribing large audio file ({file_size_mb:.1f}MB) - this may take a while...",
                    "error": None,
                }
            else:
                processing_status[video_id] = {
                    "status": "transcribing",
                    "progress": "Transcribing audio with Whisper...",
                    "error": None,
                }
        
        # Step 2: Transcribe all audio chunks IN PARALLEL for speed
        async def transcribe_chunk(index: int, audio_path: str):
            """Helper function to transcribe a single chunk."""
            try:
                processing_status[video_id] = {
                    "status": "transcribing",
                    "progress": f"Transcribing chunk {index + 1}/{len(audio_paths)}...",
                    "error": None,
                }
                transcript = await transcribe_audio(audio_path)
                
                # Clean up chunk file immediately after transcription
                try:
                    if audio_path and os.path.exists(audio_path):
                        os.remove(audio_path)
                except:
                    pass
                
                return transcript
            except Exception as e:
                print(f"⚠️ Error transcribing chunk {index + 1}: {e}")
                return None
        
        # Transcribe all chunks in parallel for maximum speed
        if len(audio_paths) > 1:
            # Parallel transcription for multiple chunks
            tasks = [transcribe_chunk(i, path) for i, path in enumerate(audio_paths)]
            transcripts = await asyncio.gather(*tasks)
            # Filter out None results (failed chunks)
            transcripts = [t for t in transcripts if t is not None]
        else:
            # Single file transcription
            transcripts = [await transcribe_audio(audio_paths[0])]
            # Clean up
            try:
                if audio_paths[0] and os.path.exists(audio_paths[0]):
                    os.remove(audio_paths[0])
            except:
                pass
        
        if not transcripts:
            raise Exception("Failed to transcribe any audio chunks")
        
        # Combine all transcripts
        transcript = "\n\n".join(transcripts)
        
        if len(audio_paths) > 1:
            print(f"✅ Successfully transcribed and combined {len(transcripts)} chunks")
        
        # Update status: generating notes
        processing_status[video_id] = {
            "status": "generating_notes",
            "progress": "Generating structured notes with GPT...",
            "error": None,
        }
        
        # Step 3: Generate notes
        notes = await generate_notes(transcript)
        
        # Step 4: Update database with results
        await update_video(
            db_pool,
            UUID(video_id),
            title=metadata.get("title"),
            transcript=transcript,
            original_notes=notes,
            duration_seconds=metadata.get("duration"),
            thumbnail_url=metadata.get("thumbnail_url"),
        )
        
        # Update status: completed
        processing_status[video_id] = {
            "status": "completed",
            "progress": "Processing completed successfully",
            "error": None,
        }
        
    except Exception as e:
        # Update status: failed
        processing_status[video_id] = {
            "status": "failed",
            "progress": None,
            "error": str(e),
        }
        raise
    
    finally:
        # Clean up audio files (chunks are already cleaned up above)
        # This is a fallback for single-file downloads
        if 'audio_paths' in locals():
            for path in audio_paths:
                if path and os.path.exists(path):
                    try:
                        os.remove(path)
                    except Exception:
                        pass  # Ignore cleanup errors


async def translate_notes_task(video_id: str, target_language: str) -> dict:
    """
    Translate notes for a video to target language.
    Checks cache first, generates if missing.
    
    Returns:
        dict with translation_id, video_id, target_language, translated_notes, created_at, was_cached
    """
    from datetime import datetime
    from uuid import UUID
    
    db_pool = await get_db_pool()
    from app.db.crud import (
        get_video_by_id,
        translation_exists,
        get_translation,
        insert_translation,
    )
    from app.openai_client import translate_text
    
    try:
        # Get video to access notes
        video = await get_video_by_id(db_pool, UUID(video_id))
        if not video:
            raise ValueError(f"Video {video_id} not found")
        
        # Check if translation already exists (cache)
        existing_translation = await translation_exists(db_pool, UUID(video_id), target_language)
        
        if existing_translation:
            translation_data = await get_translation(db_pool, UUID(video_id), target_language)
            return {
                "translation_id": str(translation_data["id"]),
                "video_id": video_id,
                "target_language": target_language,
                "translated_notes": translation_data["translated_notes"],
                "created_at": translation_data["created_at"].isoformat(),
                "was_cached": True,
            }
        
        # Translation doesn't exist, generate it
        original_notes = video.get("original_notes") or ""
        if not original_notes:
            raise ValueError("Video has no notes to translate")
        
        # Translate the notes
        translated_notes = await translate_text(original_notes, target_language)
        
        # Store translation in database
        translation_id = await insert_translation(
            db_pool,
            UUID(video_id),
            target_language,
            translated_notes,
        )
        
        return {
            "translation_id": str(translation_id),
            "video_id": video_id,
            "target_language": target_language,
            "translated_notes": translated_notes,
            "created_at": datetime.now().isoformat(),
            "was_cached": False,
        }
        
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")


# Export processing_status for use in main.py
__all__ = ["process_video_task", "translate_notes_task", "processing_status"]
