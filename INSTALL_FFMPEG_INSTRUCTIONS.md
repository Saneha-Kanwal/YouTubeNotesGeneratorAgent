# Install FFmpeg - Instructions

## 🚀 Quick Install

Run this command in your terminal:

```bash
sudo apt update && sudo apt install -y ffmpeg
```

Or use the provided script:

```bash
bash install_ffmpeg.sh
```

## 📋 Manual Installation

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y ffmpeg
```

### Fedora/RHEL/CentOS:
```bash
sudo dnf install -y ffmpeg
# or
sudo yum install -y ffmpeg
```

### macOS:
```bash
brew install ffmpeg
```

## ✅ Verify Installation

After installation, verify it works:

```bash
ffmpeg -version
```

You should see version information.

## 🎯 Why FFmpeg is Needed

FFmpeg is required for:
- **Audio compression**: Reduces large audio files to fit OpenAI's 25MB limit
- **Format conversion**: Converts audio to optimal formats for transcription
- **Quality optimization**: Balances file size and audio quality

## 🔄 After Installation

1. Restart the backend server
2. Try processing your video again
3. The system will automatically compress large files

## ⚠️ Note

If you can't install ffmpeg, you can still use the app, but:
- Very long videos (>2-3 hours) may fail
- The system will show a clear error message
- Consider using shorter video segments

