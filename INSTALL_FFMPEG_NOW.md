# 🚀 Install FFmpeg - Required for Large Videos

## ⚠️ Current Error
Your video audio file is **148.60MB**, which exceeds OpenAI's 25MB limit. FFmpeg is needed to compress it.

## 📦 Installation Command

**Run this command in your terminal:**

```bash
sudo apt update && sudo apt install -y ffmpeg
```

You will be prompted for your password. Enter it and the installation will proceed.

## ✅ Verify Installation

After installation, verify it works:

```bash
ffmpeg -version
```

You should see version information like:
```
ffmpeg version 4.x.x
```

## 🔄 After Installation

1. **Restart the backend** (if running):
   ```bash
   pkill -f "uvicorn app.main:app"
   cd /home/sanehakanwal/Documents/fista/YouTubeNotesGeneratorAgent/backend
   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Try processing your video again** - it will automatically compress the 148MB file to under 25MB

## 🎯 What FFmpeg Does

- **Compresses audio**: Reduces 148MB → <25MB automatically
- **Optimizes quality**: Balances file size and transcription accuracy
- **Handles large files**: Can process videos up to several hours long

## 📝 Alternative: Use Installation Script

You can also use the provided script:

```bash
bash /home/sanehakanwal/Documents/fista/YouTubeNotesGeneratorAgent/install_ffmpeg.sh
```

## ⚡ Quick Copy-Paste

Just copy and paste this into your terminal:

```bash
sudo apt update && sudo apt install -y ffmpeg && ffmpeg -version
```

