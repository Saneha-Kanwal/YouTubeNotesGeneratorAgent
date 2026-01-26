# Installing FFmpeg (Optional)

FFmpeg is optional but recommended for better audio quality. The app will work without it, but will use native audio formats.

## Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y ffmpeg
```

## macOS

```bash
brew install ffmpeg
```

## Verify Installation

```bash
ffmpeg -version
```

## What happens without FFmpeg?

- The app will download audio in native format (m4a, webm, etc.)
- Audio quality may vary
- Processing will still work, but may be slightly slower

The app automatically detects if FFmpeg is available and uses it if present.


