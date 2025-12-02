#!/bin/bash
# Install ffmpeg for audio compression

echo "🔧 Installing ffmpeg..."
echo ""

# Check if already installed
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is already installed!"
    ffmpeg -version | head -1
    exit 0
fi

# Install based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Detected Linux system"
    
    # Check if apt is available (Debian/Ubuntu)
    if command -v apt &> /dev/null; then
        echo "Installing via apt..."
        sudo apt update
        sudo apt install -y ffmpeg
    # Check if yum is available (RHEL/CentOS)
    elif command -v yum &> /dev/null; then
        echo "Installing via yum..."
        sudo yum install -y ffmpeg
    # Check if dnf is available (Fedora)
    elif command -v dnf &> /dev/null; then
        echo "Installing via dnf..."
        sudo dnf install -y ffmpeg
    else
        echo "❌ Package manager not found. Please install ffmpeg manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 Detected macOS"
    if command -v brew &> /dev/null; then
        echo "Installing via Homebrew..."
        brew install ffmpeg
    else
        echo "❌ Homebrew not found. Please install Homebrew first or install ffmpeg manually."
        exit 1
    fi
else
    echo "❌ Unsupported OS. Please install ffmpeg manually."
    exit 1
fi

# Verify installation
if command -v ffmpeg &> /dev/null; then
    echo ""
    echo "✅ ffmpeg installed successfully!"
    ffmpeg -version | head -1
    echo ""
    echo "🎉 You can now process large video files!"
else
    echo ""
    echo "❌ Installation failed. Please install ffmpeg manually."
    exit 1
fi

