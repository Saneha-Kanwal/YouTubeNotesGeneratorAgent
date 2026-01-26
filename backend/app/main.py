"""
FastAPI main application file.
"""
import os
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.schemas import (
    ProcessVideoRequest,
    ProcessVideoResponse,
    VideoResponse,
    VideoStatusResponse,
    VideoListResponse,
    TranslateRequest,
    TranslateResponse,
    TranslationListResponse,
    ErrorResponse,
)
from app.db.crud import get_db_pool
from app.utils import validate_youtube_url, format_error_response

# Load environment variables
load_dotenv()

# Global database pool
db_pool: asyncpg.Pool | None = None
processing_status: dict[str, dict] = {}  # In-memory status tracking


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global db_pool
    
    # Startup
    db_pool = await get_db_pool()
    yield
    
    # Shutdown
    if db_pool:
        await db_pool.close()


app = FastAPI(
    title="YouTube Notes AI Agent API",
    version="1.0.0",
    description="API for processing YouTube videos and generating structured notes",
    lifespan=lifespan,
)

# CORS configuration - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for consistent error responses."""
    import traceback
    error_detail = str(exc)
    traceback_str = traceback.format_exc() if os.getenv("DEBUG", "False").lower() == "true" else None
    
    # Log the error for debugging
    print(f"ERROR: {error_detail}")
    if traceback_str:
        print(f"TRACEBACK: {traceback_str}")
    
    return JSONResponse(
        status_code=500,
        content=format_error_response(
            "internal_error",
            f"An internal server error occurred: {error_detail}",
            {"traceback": traceback_str} if traceback_str else None,
        ),
    )


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "YouTube Notes AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/favicon.ico")
async def favicon():
    """Favicon endpoint to prevent 404 errors."""
    # Return a simple response instead of file to avoid file not found errors
    return JSONResponse({"status": "ok"})


@app.post("/process-video", response_model=ProcessVideoResponse)
async def process_video(
    request: ProcessVideoRequest,
    background_tasks: BackgroundTasks,
):
    """
    Process a YouTube video and generate notes.
    Validates URL, creates video record, and enqueues background processing.
    """
    try:
        # Check database connection
        if not db_pool:
            print("ERROR: Database pool not initialized")
            raise HTTPException(
                status_code=500, 
                detail="Database not initialized. Please check database connection."
            )
        
        # Validate YouTube URL
        youtube_url_str = str(request.youtube_url).strip()
        if not youtube_url_str:
            raise HTTPException(
                status_code=400,
                detail=format_error_response("invalid_url", "YouTube URL cannot be empty"),
            )
        
        is_valid, error_msg = validate_youtube_url(youtube_url_str)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=format_error_response("invalid_url", error_msg or "Invalid YouTube URL"),
            )
        
        # Import here to avoid circular dependency
        from app.worker import process_video_task, processing_status
        
        # Create video record (or get existing one)
        from app.db.crud import insert_video, get_video_by_url
        from uuid import UUID
        try:
            # Check if video already exists
            existing_video = await get_video_by_url(db_pool, youtube_url_str)
            if existing_video:
                video_id = existing_video["id"]
                print(f"✅ Using existing video record: {video_id}")
            else:
                video_id = await insert_video(db_pool, youtube_url_str)
                print(f"✅ Created new video record: {video_id}")
        except asyncpg.exceptions.UniqueViolationError:
            # Video already exists, get it
            existing_video = await get_video_by_url(db_pool, youtube_url_str)
            if existing_video:
                video_id = existing_video["id"]
                print(f"✅ Video already exists, using: {video_id}")
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Video URL already exists but could not retrieve it"
                )
        except asyncpg.exceptions.PostgresError as e:
            print(f"❌ Database error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            print(f"❌ Error creating video record: {str(e)}")
            import traceback
            print(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create video record: {str(e)}"
            )
        
        # Initialize processing status
        processing_status[str(video_id)] = {
            "status": "pending",
            "progress": "Video queued for processing...",
            "error": None,
        }
        
        # Enqueue background task (non-blocking)
        try:
            background_tasks.add_task(process_video_task, str(video_id), youtube_url_str)
            print(f"✅ Background task queued for video: {video_id}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to queue background task: {str(e)}")
            # Update status to indicate task queuing failed
            processing_status[str(video_id)] = {
                "status": "pending",
                "progress": "Task queued (with warnings)",
                "error": f"Background task queuing warning: {str(e)}",
            }
        
        return ProcessVideoResponse(
            video_id=video_id,
            status="pending",
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e)
        traceback_str = traceback.format_exc()
        print(f"❌ ERROR in process_video endpoint: {error_detail}")
        print(f"TRACEBACK: {traceback_str}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process video: {error_detail}"
        )


@app.get("/videos/{video_id}/status", response_model=VideoStatusResponse)
async def get_video_status(video_id: str):
    """Get video processing status."""
    from app.worker import processing_status
    status_info = processing_status.get(video_id, {"status": "unknown"})
    return VideoStatusResponse(
        video_id=video_id,
        status=status_info.get("status", "unknown"),
        progress=status_info.get("progress"),
        error=status_info.get("error"),
    )


@app.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """Get video details and notes."""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    from uuid import UUID
    try:
        video_uuid = UUID(video_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    
    from app.db.crud import get_video_by_id
    video = await get_video_by_id(db_pool, video_uuid)
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return VideoResponse(**video)


@app.get("/videos", response_model=VideoListResponse)
async def list_videos(page: int = 1, limit: int = 20):
    """List all processed videos with pagination."""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    from app.db.crud import list_videos
    videos, total = await list_videos(db_pool, page, limit)
    
    return VideoListResponse(
        videos=videos,
        total=total,
        page=page,
        limit=limit,
    )


@app.delete("/videos/{video_id}")
async def delete_video(video_id: str):
    """Delete a video and its translations."""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    from uuid import UUID
    try:
        video_uuid = UUID(video_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    
    from app.db.crud import delete_video
    deleted = await delete_video(db_pool, video_uuid)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Remove from status tracking
    from app.worker import processing_status
    processing_status.pop(video_id, None)
    
    return {"message": "Video deleted successfully"}


@app.post("/translate", response_model=TranslateResponse)
async def translate_notes(request: TranslateRequest):
    """
    Translate notes to a target language.
    Returns existing translation if available, otherwise generates new one.
    """
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    # Validate language code
    from app.utils import validate_language_code
    is_valid, error_msg = validate_language_code(request.target_language)
    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=format_error_response("invalid_language", error_msg or "Invalid language code"),
        )
    
    from app.worker import translate_notes_task
    result = await translate_notes_task(
        str(request.video_id),
        request.target_language,
    )
    
    return TranslateResponse(**result)


@app.get("/videos/{video_id}/translations", response_model=TranslationListResponse)
async def get_video_translations(video_id: str):
    """Get all translations for a video."""
    if not db_pool:
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    from uuid import UUID
    try:
        video_uuid = UUID(video_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid video ID format")
    
    from app.db.crud import list_translations
    translations = await list_translations(db_pool, video_uuid)
    
    return TranslationListResponse(translations=translations)

