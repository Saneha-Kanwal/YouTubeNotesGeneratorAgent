"""
Audio chunking utility for splitting large audio files into smaller chunks.
Enables processing of very long videos by splitting them into 25MB chunks.
"""
import os
import subprocess
from pathlib import Path
from typing import List


def get_ffmpeg_env():
    """Get environment with FFmpeg in PATH."""
    import os
    env = os.environ.copy()
    home_dir = os.path.expanduser("~")
    local_bin = f"{home_dir}/.local/bin"
    current_path = env.get("PATH", "")
    if local_bin not in current_path:
        env["PATH"] = f"{local_bin}:{current_path}"
    if "/usr/bin" not in env["PATH"]:
        env["PATH"] = f"{env['PATH']}:/usr/bin:/bin"
    return env


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds using ffprobe or ffmpeg."""
    try:
        env = get_ffmpeg_env()
        # Try ffprobe first
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                audio_path
            ],
            capture_output=True,
            text=True,
            timeout=10,
            env=env
        )
        if result.returncode == 0:
            return float(result.stdout.strip())
        
        # Fallback to ffmpeg if ffprobe not available
        result = subprocess.run(
            [
                "ffmpeg", "-i", audio_path
            ],
            capture_output=True,
            text=True,
            timeout=10,
            env=env
        )
        # Parse duration from ffmpeg output
        import re
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', result.stderr)
        if duration_match:
            hours, minutes, seconds, centiseconds = map(int, duration_match.groups())
            return hours * 3600 + minutes * 60 + seconds + centiseconds / 100
    except Exception as e:
        print(f"⚠️ Could not get audio duration: {e}")
    return 0.0


def split_audio_into_chunks(
    audio_path: str,
    max_chunk_size_mb: float = 20.0,  # 20MB to be safe (under 25MB limit)
    output_dir: Path = None
) -> List[str]:
    """
    Split audio file into chunks that are under max_chunk_size_mb.
    
    Args:
        audio_path: Path to audio file
        max_chunk_size_mb: Maximum size per chunk in MB (default 20MB)
        output_dir: Directory to save chunks (default: same as audio file)
    
    Returns:
        List of chunk file paths
    """
    if output_dir is None:
        output_dir = Path(audio_path).parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    audio_file = Path(audio_path)
    base_name = audio_file.stem
    chunks = []
    
    # Get file size and duration
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    duration = get_audio_duration(audio_path)
    
    if file_size_mb <= max_chunk_size_mb:
        # File is already small enough
        return [audio_path]
    
    print(f"📦 Splitting {file_size_mb:.2f}MB audio file into chunks...")
    
    # Calculate number of chunks needed (add 20% buffer for safety)
    num_chunks = int((file_size_mb / max_chunk_size_mb) * 1.2) + 1
    chunk_duration = duration / num_chunks if duration > 0 and num_chunks > 0 else 0
    
    # If we can't determine duration, estimate based on file size
    if duration <= 0:
        # Estimate: assume ~1MB per minute at 64kbps
        estimated_duration = file_size_mb * 60  # rough estimate
        chunk_duration = estimated_duration / num_chunks if num_chunks > 0 else 300  # default 5 min chunks
        print(f"⚠️ Could not determine duration, estimating {estimated_duration:.0f} seconds")
    
    env = get_ffmpeg_env()
    
    # Split into chunks
    for i in range(num_chunks):
        chunk_path = output_dir / f"{base_name}_chunk_{i:03d}.mp3"
        start_time = i * chunk_duration
        
        # Build ffmpeg command
        cmd = [
            "ffmpeg",
            "-i", audio_path,
            "-ss", str(start_time),
            "-acodec", "libmp3lame",
            "-ab", "64k",  # Low bitrate for chunks
            "-ar", "16000",  # Lower sample rate
            "-ac", "1",  # Mono
        ]
        
        # Add duration limit for all chunks except the last one
        if i < num_chunks - 1 and chunk_duration > 0:
            cmd.extend(["-t", str(chunk_duration)])
        # Last chunk gets remaining audio (no -t flag)
        
        cmd.extend(["-y", str(chunk_path)])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=600,
                env=env
            )
            
            if result.returncode == 0 and chunk_path.exists():
                chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
                
                # If chunk is still too large, compress it further
                if chunk_size > max_chunk_size_mb:
                    print(f"⚠️ Chunk {i+1} too large ({chunk_size:.2f}MB), compressing...")
                    compressed_chunk = output_dir / f"{base_name}_chunk_{i:03d}_compressed.mp3"
                    compress_result = subprocess.run(
                        [
                            "ffmpeg", "-i", str(chunk_path),
                            "-acodec", "libmp3lame",
                            "-ab", "32k",  # Very low bitrate
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
                        chunk_path.unlink()  # Remove original
                        chunk_path = compressed_chunk
                        chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
                        print(f"✅ Chunk {i+1} compressed to {chunk_size:.2f}MB")
                
                chunks.append(str(chunk_path))
                print(f"✅ Created chunk {i+1}/{num_chunks} ({chunk_size:.2f}MB)")
            else:
                error_msg = result.stderr.decode() if result.stderr else "Unknown error"
                print(f"⚠️ Failed to create chunk {i+1}: {error_msg}")
        except Exception as e:
            print(f"⚠️ Error creating chunk {i+1}: {e}")
            continue
    
    if not chunks:
        raise Exception("Failed to create any audio chunks")
    
    print(f"✅ Successfully split audio into {len(chunks)} chunks")
    return chunks

