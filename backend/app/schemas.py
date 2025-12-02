"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class ProcessVideoRequest(BaseModel):
    """Request schema for processing a YouTube video."""
    youtube_url: HttpUrl = Field(..., description="Valid YouTube video URL")


class ProcessVideoResponse(BaseModel):
    """Response schema for video processing initiation."""
    video_id: UUID
    status: str = Field(..., description="Current processing status")


class VideoResponse(BaseModel):
    """Response schema for video details."""
    id: UUID
    youtube_url: str
    title: Optional[str] = None
    transcript: Optional[str] = None
    original_notes: Optional[str] = None
    duration_seconds: Optional[int] = None
    thumbnail_url: Optional[str] = None
    created_at: datetime


class VideoStatusResponse(BaseModel):
    """Response schema for video processing status."""
    video_id: UUID
    status: str = Field(..., description="Processing status")
    progress: Optional[str] = None
    error: Optional[str] = None


class VideoSummary(BaseModel):
    """Summary schema for video list."""
    id: UUID
    youtube_url: str
    title: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    created_at: datetime


class VideoListResponse(BaseModel):
    """Response schema for video list."""
    videos: List[VideoSummary]
    total: int
    page: int
    limit: int


class TranslateRequest(BaseModel):
    """Request schema for translating notes."""
    video_id: UUID = Field(..., description="Video to translate")
    target_language: str = Field(..., pattern="^[a-z]{2}$", description="ISO 639-1 language code")


class TranslateResponse(BaseModel):
    """Response schema for translation."""
    translation_id: UUID
    video_id: UUID
    target_language: str
    translated_notes: str
    created_at: datetime
    was_cached: bool = Field(..., description="Whether translation was retrieved from cache")


class TranslationSummary(BaseModel):
    """Summary schema for translation list."""
    id: UUID
    target_language: str
    created_at: datetime


class TranslationListResponse(BaseModel):
    """Response schema for translation list."""
    translations: List[TranslationSummary]


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    message: str
    details: Optional[dict] = None

