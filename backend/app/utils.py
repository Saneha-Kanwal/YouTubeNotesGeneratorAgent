"""
Utility functions for URL validation, error formatting, etc.
"""
import re
from typing import Optional
from urllib.parse import urlparse


def validate_youtube_url(url: str) -> tuple[bool, Optional[str]]:
    """
    Validate YouTube URL format and domain.
    Returns (is_valid, error_message).
    """
    if not url:
        return False, "URL cannot be empty"
    
    # Parse URL
    try:
        parsed = urlparse(str(url))
    except Exception:
        return False, "Invalid URL format"
    
    # Check domain
    valid_domains = [
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
        "m.youtube.com",
    ]
    
    domain = parsed.netloc.lower()
    if not any(domain == d or domain.endswith(f".{d}") for d in valid_domains):
        return False, f"URL must be from YouTube domain. Got: {domain}"
    
    # Check for video ID in path
    if parsed.hostname == "youtu.be":
        # Short URL format: youtu.be/VIDEO_ID
        video_id_match = re.match(r"^/([a-zA-Z0-9_-]{11})", parsed.path)
    else:
        # Standard URL format: youtube.com/watch?v=VIDEO_ID
        video_id_match = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", parsed.query)
    
    if not video_id_match:
        return False, "URL must contain a valid YouTube video ID"
    
    return True, None


def format_error_response(error_type: str, message: str, details: Optional[dict] = None) -> dict:
    """Format error response consistently."""
    response = {
        "error": error_type,
        "message": message,
    }
    if details:
        response["details"] = details
    return response


def validate_language_code(lang_code: str) -> tuple[bool, Optional[str]]:
    """
    Validate language code (supports ISO 639-1 and extended codes like zh-TW).
    Returns (is_valid, error_message).
    """
    if not lang_code:
        return False, "Language code cannot be empty"
    
    # Support extended codes like zh-TW
    if '-' in lang_code:
        parts = lang_code.split('-')
        if len(parts) != 2:
            return False, "Invalid language code format"
        base_code, region = parts
        if not (base_code.isalpha() and base_code.islower() and len(base_code) == 2):
            return False, "Invalid base language code"
        if not (region.isalpha() and region.isupper() and len(region) == 2):
            return False, "Invalid region code"
        return True, None
    
    # Standard ISO 639-1 (2 characters)
    if len(lang_code) != 2:
        return False, "Language code must be 2 characters (ISO 639-1) or extended format (e.g., zh-TW)"
    
    if not lang_code.isalpha() or not lang_code.islower():
        return False, "Language code must be lowercase letters only"
    
    return True, None

