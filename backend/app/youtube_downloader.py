"""
YouTube audio downloader using yt-dlp.
"""
import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import yt_dlp


async def download_audio(youtube_url: str) -> tuple[str, Dict[str, Any]]:
    """
    Download audio from YouTube video and extract metadata.
    
    Returns:
        tuple: (audio_file_path, metadata_dict)
        metadata_dict contains: title, duration, thumbnail_url
    """
    # Create temporary directory for audio files
    audio_dir = Path("audio_cache")
    audio_dir.mkdir(exist_ok=True)
    
    # Configure yt-dlp options
    # Use format that doesn't require postprocessing if ffmpeg is not available
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
        "outtmpl": str(audio_dir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    
    # Only add postprocessor if ffmpeg is available
    # Use lower bitrate to reduce file size (OpenAI limit is 25MB)
    ffmpeg_available = False
    try:
        import subprocess
        import os
        # Check FFmpeg in PATH (including user local bin)
        env = os.environ.copy()
        home_dir = os.path.expanduser("~")
        local_bin = f"{home_dir}/.local/bin"
        if local_bin not in env.get("PATH", ""):
            env["PATH"] = f"{local_bin}:{env.get('PATH', '')}"
        
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
                "preferredquality": "128",  # Lower quality to reduce file size (was 192)
            }]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # ffmpeg not available, use native audio format
        pass
    
    metadata = {}
    audio_path = None
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info
            info = ydl.extract_info(youtube_url, download=True)
            
            # Get metadata
            metadata = {
                "title": info.get("title"),
                "duration": info.get("duration"),  # in seconds
                "thumbnail_url": info.get("thumbnail"),
            }
            
            # Find downloaded file
            video_id = info.get("id")
            if video_id:
                # yt-dlp downloads as mp3 after postprocessing
                audio_path = str(audio_dir / f"{video_id}.mp3")
                if not os.path.exists(audio_path):
                    # Try to find the file with any extension
                    for ext in ["mp3", "m4a", "webm", "opus"]:
                        candidate = audio_dir / f"{video_id}.{ext}"
                        if candidate.exists():
                            audio_path = str(candidate)
                            break
            
            if not audio_path or not os.path.exists(audio_path):
                raise FileNotFoundError(f"Downloaded audio file not found for video {video_id}")
            
            # Check file size and compress if needed (OpenAI limit is 25MB)
            MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB in bytes
            file_size = os.path.getsize(audio_path)
            
            if file_size > MAX_FILE_SIZE:
                print(f"⚠️ Audio file too large ({file_size / 1024 / 1024:.2f}MB), compressing...")
                if ffmpeg_available:
                    # Compress the audio file with aggressive settings
                    compressed_path = str(audio_dir / f"{video_id}_compressed.mp3")
                    import subprocess
                    
                    # Calculate target bitrate based on file size
                    # For very large files, use even lower bitrate
                    # More aggressive compression for files > 50MB
                    if file_size > 100 * 1024 * 1024:  # > 100MB
                        bitrate = "48k"  # Ultra low for huge files
                        sample_rate = "16000"  # Lower sample rate
                    elif file_size > 50 * 1024 * 1024:  # > 50MB (like 55MB)
                        bitrate = "64k"  # More aggressive for 50-100MB files
                        sample_rate = "16000"  # Lower sample rate
                    else:
                        bitrate = "80k"
                        sample_rate = "22050"
                    
                    # Ensure FFmpeg is in PATH (check both system and user local bin)
                    import os
                    env = os.environ.copy()
                    home_dir = os.path.expanduser("~")
                    local_bin = f"{home_dir}/.local/bin"
                    current_path = env.get("PATH", "")
                    if local_bin not in current_path:
                        env["PATH"] = f"{local_bin}:{current_path}"
                    # Also ensure system paths are available
                    if "/usr/bin" not in env["PATH"]:
                        env["PATH"] = f"{env['PATH']}:/usr/bin:/bin"
                    
                    print(f"🔧 Compressing {file_size / 1024 / 1024:.2f}MB file with {bitrate} bitrate and {sample_rate}Hz sample rate...")
                    result = subprocess.run(
                        [
                            "ffmpeg", "-i", audio_path,
                            "-acodec", "libmp3lame",
                            "-ab", bitrate,
                            "-ar", sample_rate,
                            "-ac", "1",  # Mono channel for smaller size
                            "-compression_level", "2",  # Higher compression
                            "-y",  # Overwrite output file
                            compressed_path
                        ],
                        capture_output=True,
                        timeout=600,  # 10 minute timeout for large files
                        env=env  # Use modified environment with FFmpeg in PATH
                    )
                    if result.returncode == 0 and os.path.exists(compressed_path):
                        # Remove original and use compressed
                        try:
                            os.remove(audio_path)
                        except:
                            pass
                        audio_path = compressed_path
                        new_size = os.path.getsize(audio_path)
                        print(f"✅ Compressed to {new_size / 1024 / 1024:.2f}MB")
                        
                        # If still too large, try even more aggressive compression
                        if new_size > MAX_FILE_SIZE:
                            print(f"⚠️ Still too large ({new_size / 1024 / 1024:.2f}MB), applying ultra compression...")
                            ultra_compressed = str(audio_dir / f"{video_id}_ultra_compressed.mp3")
                            
                            # Even more aggressive settings
                            ultra_bitrate = "40k" if new_size > 30 * 1024 * 1024 else "48k"
                            result2 = subprocess.run(
                                [
                                    "ffmpeg", "-i", audio_path,
                                    "-acodec", "libmp3lame",
                                    "-ab", ultra_bitrate,  # Ultra low bitrate
                                    "-ar", "16000",  # Very low sample rate
                                    "-ac", "1",  # Mono
                                    "-compression_level", "2",  # Higher compression
                                    "-y",
                                    ultra_compressed
                                ],
                                capture_output=True,
                                timeout=600,
                                env=env
                            )
                            if result2.returncode == 0 and os.path.exists(ultra_compressed):
                                try:
                                    os.remove(audio_path)
                                except:
                                    pass
                                audio_path = ultra_compressed
                                final_size = os.path.getsize(audio_path)
                                print(f"✅ Ultra compressed to {final_size / 1024 / 1024:.2f}MB")
                                
                                # Final check - if still too large, try one more time with minimal settings
                                if final_size > MAX_FILE_SIZE:
                                    print(f"⚠️ Still too large ({final_size / 1024 / 1024:.2f}MB), applying minimal compression...")
                                    minimal_compressed = str(audio_dir / f"{video_id}_minimal.mp3")
                                    result3 = subprocess.run(
                                        [
                                            "ffmpeg", "-i", audio_path,
                                            "-acodec", "libmp3lame",
                                            "-ab", "32k",  # Minimal bitrate
                                            "-ar", "16000",
                                            "-ac", "1",
                                            "-compression_level", "2",
                                            "-y",
                                            minimal_compressed
                                        ],
                                        capture_output=True,
                                        timeout=600,
                                        env=env
                                    )
                                    if result3.returncode == 0 and os.path.exists(minimal_compressed):
                                        try:
                                            os.remove(audio_path)
                                        except:
                                            pass
                                        audio_path = minimal_compressed
                                        minimal_size = os.path.getsize(audio_path)
                                        print(f"✅ Minimal compressed to {minimal_size / 1024 / 1024:.2f}MB")
                                        
                                        if minimal_size > MAX_FILE_SIZE:
                                            # Don't raise error - let chunking handle it
                                            print(f"⚠️ File still large ({minimal_size / 1024 / 1024:.2f}MB) after compression.")
                                            print(f"📦 Will use audio chunking to process this large file.")
                                            # Continue with the compressed file - chunking will handle it
                            else:
                                error_msg2 = result2.stderr.decode() if result2.stderr else "Unknown error"
                                print(f"⚠️ Ultra compression failed: {error_msg2}")
                                if new_size > MAX_FILE_SIZE:
                                    raise Exception(
                                        f"Compression failed. File size: {new_size / 1024 / 1024:.2f}MB. "
                                        f"Please use a shorter video."
                                    )
                    else:
                        error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                        print(f"⚠️ Compression failed: {error_msg}")
                        raise Exception(f"Compression failed: {error_msg}")
                else:
                    raise Exception(
                        f"Audio file too large ({file_size / 1024 / 1024:.2f}MB) and ffmpeg not available.\n\n"
                        f"📦 To install ffmpeg, run:\n"
                        f"   sudo apt update && sudo apt install -y ffmpeg\n\n"
                        f"Or use a shorter video (< 2 hours recommended)."
                    )
            
    except Exception as e:
        raise Exception(f"Failed to download audio: {str(e)}")
    
    return audio_path, metadata

