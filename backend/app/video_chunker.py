"""
Video chunking utility for splitting long YouTube videos into smaller segments.
Downloads full video first, then splits into 10-15 minute chunks for processing.
"""
import yt_dlp
from pathlib import Path
from typing import List, Dict, Any, Tuple
import os
import subprocess


def get_video_duration(youtube_url: str) -> float:
    """
    Get video duration in seconds without downloading.
    
    Returns:
        Duration in seconds, or 0 if unable to determine
    """
    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            duration = info.get("duration", 0)
            return float(duration) if duration else 0.0
    except Exception as e:
        print(f"⚠️ Could not get video duration: {e}")
        return 0.0


def get_ffmpeg_env():
    """Get environment with FFmpeg in PATH."""
    env = os.environ.copy()
    home_dir = os.path.expanduser("~")
    local_bin = f"{home_dir}/.local/bin"
    current_path = env.get("PATH", "")
    if local_bin not in current_path:
        env["PATH"] = f"{local_bin}:{current_path}"
    if "/usr/bin" not in env["PATH"]:
        env["PATH"] = f"{env['PATH']}:/usr/bin:/bin"
    return env


def split_audio_file_into_chunks(
    audio_path: str,
    chunk_duration_seconds: float,
    num_chunks: int,
    total_duration: float,
    video_id: str,
    output_dir: Path
) -> List[str]:
    """
    Split downloaded audio file into time-based chunks.
    
    Args:
        audio_path: Path to full audio file
        chunk_duration_seconds: Duration of each chunk in seconds
        num_chunks: Total number of chunks to create
        total_duration: Total duration of audio in seconds
        video_id: Video ID for naming chunks
        output_dir: Directory to save chunks
    
    Returns:
        List of chunk file paths
    """
    env = get_ffmpeg_env()
    chunk_paths = []
    
    for i in range(num_chunks):
        start_time = i * chunk_duration_seconds
        # Last chunk gets remaining time
        if i == num_chunks - 1:
            duration = total_duration - start_time
        else:
            duration = chunk_duration_seconds
        
        chunk_path = output_dir / f"{video_id}_chunk_{i:03d}.mp3"
        
        print(f"📦 Creating chunk {i+1}/{num_chunks} ({start_time:.0f}s - {start_time + duration:.0f}s)...")
        
        # Build ffmpeg command to extract chunk
        cmd = [
            "ffmpeg",
            "-i", audio_path,
            "-ss", str(start_time),
            "-acodec", "libmp3lame",
            "-ab", "128k",  # Bitrate
            "-ar", "22050",  # Sample rate
            "-ac", "1",  # Mono channel
        ]
        
        # Add duration limit for all chunks except the last one
        if i < num_chunks - 1:
            cmd.extend(["-t", str(chunk_duration_seconds)])
        # Last chunk gets remaining audio (no -t flag)
        
        cmd.extend(["-y", str(chunk_path)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300,  # 5 minute timeout per chunk
                env=env
            )
            
            if result.returncode == 0 and chunk_path.exists():
                chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
                
                # Compress chunk if too large (over 25MB limit)
                if chunk_size > 25:
                    print(f"⚠️ Chunk {i+1} too large ({chunk_size:.2f}MB), compressing...")
                    compressed_chunk = output_dir / f"{video_id}_chunk_{i:03d}_compressed.mp3"
                    compress_result = subprocess.run(
                        [
                            "ffmpeg", "-i", str(chunk_path),
                            "-acodec", "libmp3lame",
                            "-ab", "64k",  # Lower bitrate
                            "-ar", "16000",
                            "-ac", "1",
                            "-y",
                            str(compressed_chunk)
                        ],
                        capture_output=True,
                        timeout=300,
                        env=env
                    )
                    if compress_result.returncode == 0 and compressed_chunk.exists():
                        chunk_path.unlink()
                        chunk_path = compressed_chunk
                        chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
                        print(f"✅ Chunk {i+1} compressed to {chunk_size:.2f}MB")
                
                chunk_paths.append(str(chunk_path))
                print(f"✅ Chunk {i+1}/{num_chunks} created ({chunk_size:.2f}MB)")
            else:
                error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                print(f"⚠️ Failed to create chunk {i+1}: {error_msg[:200]}")
        except Exception as e:
            print(f"⚠️ Error creating chunk {i+1}: {e}")
            continue
    
    return chunk_paths


async def download_video_in_chunks(
    youtube_url: str,
    chunk_duration_minutes: float = 12.0  # 12 minutes per chunk (safe for 15 min limit)
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Download a long YouTube video and split it into chunks.
    
    Strategy:
    1. Check video duration
    2. If > 30 min, download full video first (using yt-dlp)
    3. Split downloaded file into time-based chunks
    4. Return list of chunk paths
    
    Args:
        youtube_url: YouTube video URL
        chunk_duration_minutes: Duration of each chunk in minutes (default 12 minutes)
    
    Returns:
        Tuple of (list of audio file paths, metadata dict)
    """
    # Step 1: Get video duration
    print(f"🔍 Checking video duration...")
    total_duration = get_video_duration(youtube_url)
    
    if total_duration == 0:
        raise Exception("Could not determine video duration")
    
    total_duration_minutes = total_duration / 60
    print(f"📊 Video duration: {total_duration_minutes:.1f} minutes ({total_duration:.0f} seconds)")
    
    # Step 2: Check if chunking is needed (> 30 minutes)
    CHUNKING_THRESHOLD = 30 * 60  # 30 minutes in seconds
    
    if total_duration <= CHUNKING_THRESHOLD:
        # Video is short enough, download normally
        print(f"✅ Video is short enough ({total_duration_minutes:.1f} min), downloading normally...")
        from app.youtube_downloader import download_audio
        audio_path, metadata = await download_audio(youtube_url)
        return [audio_path], metadata
    
    # Step 3: Video is long - download full video first, then split
    print(f"📦 Video is long ({total_duration_minutes:.1f} min), will download and split into chunks...")
    
    audio_dir = Path("audio_cache")
    audio_dir.mkdir(exist_ok=True)
    
    # Extract video info
    print(f"🔍 Extracting video information...")
    try:
        ydl_opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(youtube_url, download=False)
            video_id = video_info.get("id", "unknown")
            video_title = video_info.get("title", "Unknown")
    except Exception as e:
        raise Exception(f"Failed to extract video info: {str(e)}")
    
    # Download full video using yt-dlp (handles authentication)
    print(f"📥 Downloading full video (this may take a while for long videos)...")
    
    # Configure yt-dlp to download audio with optimized settings for speed
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
        "outtmpl": str(audio_dir / f"{video_id}_full.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,  # Faster, less output
        "extractaudio": True,
        "audioformat": "mp3",
        "audioquality": "128K",  # Lower quality for faster download
        "concurrent_fragments": 8,  # Parallel fragment downloads
        "retries": 3,
        "fragment_retries": 3,
    }
    
    # Add postprocessor if ffmpeg is available
    env = get_ffmpeg_env()
    ffmpeg_available = False
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=2,
            env=env
        )
        if result.returncode == 0:
            ffmpeg_available = True
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }]
    except:
        pass
    
    if not ffmpeg_available:
        raise Exception("FFmpeg is required for video chunking. Please install ffmpeg.")
    
    # Download the full video
    full_audio_path = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            
            # Find downloaded file
            for ext in ["mp3", "m4a", "webm", "opus"]:
                candidate = audio_dir / f"{video_id}_full.{ext}"
                if candidate.exists():
                    full_audio_path = str(candidate)
                    break
        
        if not full_audio_path or not os.path.exists(full_audio_path):
            raise Exception(f"Downloaded audio file not found for video {video_id}")
        
        file_size_mb = os.path.getsize(full_audio_path) / (1024 * 1024)
        print(f"✅ Full video downloaded ({file_size_mb:.2f}MB)")
        
    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
    
    # Step 4: Split into chunks
    chunk_duration_seconds = chunk_duration_minutes * 60
    num_chunks = int((total_duration / chunk_duration_seconds) + 0.99)  # Round up
    
    print(f"📦 Splitting into {num_chunks} chunks of ~{chunk_duration_minutes:.0f} minutes each...")
    
    chunk_paths = split_audio_file_into_chunks(
        full_audio_path,
        chunk_duration_seconds,
        num_chunks,
        total_duration,
        video_id,
        audio_dir
    )
    
    # Clean up full video file
    try:
        if os.path.exists(full_audio_path):
            os.remove(full_audio_path)
            print(f"🗑️ Cleaned up full video file")
    except:
        pass
    
    if not chunk_paths:
        raise Exception("Failed to create any video chunks")
    
    print(f"✅ Successfully created {len(chunk_paths)} chunks")
    
    metadata = {
        "title": video_title,
        "duration": total_duration,
        "thumbnail_url": video_info.get("thumbnail"),
        "total_chunks": len(chunk_paths),
    }
    
    return chunk_paths, metadata
