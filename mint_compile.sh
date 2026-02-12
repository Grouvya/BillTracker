#!/bin/bash

# =================================================================
# BillTracker Compilation Script for Linux Mint / Ubuntu
# =================================================================

# Exit on any error
set -e

echo "----------------------------------------------------"
echo "🚀 Starting BillTracker Compilation for Linux Mint"
echo "----------------------------------------------------"

# 1. Update and install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev \
    libxcb-xinerama0 libdbus-1-3 libegl1 binutils \
    libxcb-cursor0  # Additional requirement for Qt6 on some Mint versions

# 2. Set up virtual environment
echo "🐍 Setting up Python virtual environment..."
if [ -d "venv_linux" ]; then
    echo "Using existing venv_linux..."
else
    python3 -m venv venv_linux
fi
source venv_linux/bin/activate

# 3. Upgrade pip and install requirements
echo "📥 Installing Python packages..."
pip install --upgrade pip
pip install PyQt6 cryptography reportlab pyinstaller

# 4. Build the application
echo "🛠️ Building with PyInstaller..."
# We use the spec file if it exists, otherwise we generate a command
if [ -f "Billtracker_qt.spec" ]; then
    pyinstaller Billtracker_qt.spec --clean --noconfirm
else
    pyinstaller --name "BillTracker" \
                --onefile \
                --windowed \
                --icon="billtracker.png" \
                --add-data "billtracker.png:." \
                --add-data "billtracker.ico:." \
                Billtracker_qt.py
fi

echo "----------------------------------------------------"
echo "✅ Compilation Finished!"
echo "----------------------------------------------------"
echo "The executable can be found in the 'dist' folder."
echo ""
echo "To run your app, use:"
echo "./dist/Billtracker_qt (or the name defined in spec)"
echo ""
echo "Note: If you encounter 'xcb' errors, ensure you have"
echo "installed all Qt6 dependencies listed above."
echo "----------------------------------------------------"
