#!/bin/bash
# Auto-install FFmpeg script
# This script will attempt to install ffmpeg using various methods

set -e

echo "🔧 Attempting to install FFmpeg..."
echo ""

# Method 1: Try with sudo apt (requires password)
if command -v apt &> /dev/null; then
    echo "📦 Method 1: Installing via apt (requires sudo password)..."
    echo "Please enter your password when prompted:"
    if sudo apt update && sudo apt install -y ffmpeg; then
        echo "✅ FFmpeg installed successfully via apt!"
        ffmpeg -version | head -1
        exit 0
    else
        echo "❌ apt installation failed"
    fi
fi

# Method 2: Try snap (may not require sudo in some cases)
if command -v snap &> /dev/null; then
    echo "📦 Method 2: Trying snap..."
    if snap install ffmpeg 2>/dev/null; then
        echo "✅ FFmpeg installed successfully via snap!"
        ffmpeg -version | head -1
        exit 0
    else
        echo "⚠️ snap installation requires sudo or didn't work"
    fi
fi

# Method 3: Download static binary (no sudo needed)
echo "📦 Method 3: Downloading static FFmpeg binary (no sudo required)..."
FFMPEG_DIR="$HOME/.local/bin"
mkdir -p "$FFMPEG_DIR"

# Try to download from GitHub releases
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
fi

echo "Downloading FFmpeg static build for $ARCH..."
cd /tmp

# Try downloading from johnvansickle.com (popular static builds)
if wget -q --show-progress "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${ARCH}-static.tar.xz" 2>/dev/null || \
   wget -q "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${ARCH}-static.tar.xz" 2>/dev/null; then
    echo "Extracting..."
    tar -xf "ffmpeg-git-${ARCH}-static.tar.xz" 2>/dev/null || true
    if [ -f "ffmpeg-git-${ARCH}-static/ffmpeg" ]; then
        cp "ffmpeg-git-${ARCH}-static/ffmpeg" "$FFMPEG_DIR/ffmpeg"
        cp "ffmpeg-git-${ARCH}-static/ffprobe" "$FFMPEG_DIR/ffprobe" 2>/dev/null || true
        chmod +x "$FFMPEG_DIR/ffmpeg"
        chmod +x "$FFMPEG_DIR/ffprobe" 2>/dev/null || true
        rm -rf "ffmpeg-git-${ARCH}-static" "ffmpeg-git-${ARCH}-static.tar.xz"
        
        # Add to PATH if not already there
        if [[ ":$PATH:" != *":$FFMPEG_DIR:"* ]]; then
            echo "" >> "$HOME/.bashrc"
            echo "# FFmpeg static binary" >> "$HOME/.bashrc"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$HOME/.bashrc"
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        echo "✅ FFmpeg installed to $FFMPEG_DIR"
        "$FFMPEG_DIR/ffmpeg" -version | head -1
        echo ""
        echo "⚠️ Note: You may need to restart your terminal or run:"
        echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
        exit 0
    fi
fi

echo ""
echo "❌ All installation methods failed."
echo ""
echo "Please install FFmpeg manually:"
echo "   sudo apt update && sudo apt install -y ffmpeg"
exit 1

