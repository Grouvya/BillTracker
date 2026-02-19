#!/bin/bash

# =================================================================
# BillTracker Installation Script for Linux Mint / Ubuntu
# =================================================================

# Exit on any error
set -e

APP_NAME="BillTracker"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/billtracker.desktop"
ICON_DIR="/usr/share/icons/hicolor/512x512/apps"
ICON_FILE="$ICON_DIR/billtracker.png"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}----------------------------------------------------${NC}"
echo -e "${GREEN}🚀 Starting BillTracker Installation for Linux Mint${NC}"
echo -e "${GREEN}----------------------------------------------------${NC}"

# 1. Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}❌ Please run as root (use sudo).${NC}"
  exit 1
fi

# 2. Check if the build exists
if [ ! -f "dist/Billtracker_qt" ]; then
    echo -e "${RED}❌ compiled executable not found in 'dist/Billtracker_qt'.${NC}"
    echo "Please run './mint_compile.sh' first to build the application."
    exit 1
fi

# 3. Create installation directory
echo "📂 Creating installation directory: $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# 4. Install executable
echo "📦 Installing executable..."
cp "dist/Billtracker_qt" "$INSTALL_DIR/$APP_NAME"
chmod +x "$INSTALL_DIR/$APP_NAME"

# 5. Install Icon
echo "🖼️  Installing icon..."
mkdir -p "$ICON_DIR"
cp "billtracker.png" "$ICON_FILE"

# 6. Install Desktop File
echo "📝 Installing desktop entry..."

# Create a temporary desktop file with correct paths
cat > /tmp/billtracker.desktop <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=BillTracker
Comment=Personal Finance Manager - Track bills and manage budgets
Exec=$INSTALL_DIR/$APP_NAME
Icon=billtracker
Terminal=false
Categories=Office;Finance;Qt;
Keywords=finance;bills;budget;money;tracker;
StartupNotify=true
StartupWMClass=Billtracker_qt
EOF

mv /tmp/billtracker.desktop "$DESKTOP_FILE"
chmod 644 "$DESKTOP_FILE"

# 7. Update system caches
echo "🔄 Updating system databases..."
update-desktop-database /usr/share/applications
gtk-update-icon-cache /usr/share/icons/hicolor

echo -e "${GREEN}----------------------------------------------------${NC}"
echo -e "${GREEN}✅ Installation Finished!${NC}"
echo -e "${GREEN}----------------------------------------------------${NC}"
echo "You can now find BillTracker in your start menu."
echo "To uninstall, remove:"
echo "  - $INSTALL_DIR"
echo "  - $DESKTOP_FILE"
echo "  - $ICON_FILE"
echo "----------------------------------------------------"
