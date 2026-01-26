"""
SQLAlchemy models for reference only.
All database operations use raw SQL queries via asyncpg.
These models are maintained for type safety and documentation.
"""
from datetime import datetime
from uuid import UUID
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Video(Base):
    """Video model - represents a processed YouTube video."""
    __tablename__ = "videos"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    youtube_url = Column(Text, nullable=False, unique=True)
    title = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    original_notes = Column(Text, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default="now()")


class Translation(Base):
    """Translation model - represents a translated version of notes."""
    __tablename__ = "translations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()")
    video_id = Column(PGUUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False)
    target_lang = Column(Text, nullable=False)
    translated_notes = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default="now()")

    __table_args__ = (
        UniqueConstraint("video_id", "target_lang", name="uq_translations_video_lang"),
    )

