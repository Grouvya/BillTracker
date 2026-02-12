#!/bin/bash
# macOS Build Script for BillTracker

set -e  # Exit on error

VERSION="5.5.0"
APP_NAME="BillTracker"
BUILD_DIR="dist"
APP_BUNDLE="${BUILD_DIR}/Billtracker_qt.app"

echo "Building ${APP_NAME} for macOS..."

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Convert PNG icon to ICNS format (macOS requires .icns)
if [ ! -f "billtracker.icns" ]; then
    echo "Converting icon to .icns format..."
    mkdir -p billtracker.iconset
    sips -z 16 16     billtracker.png --out billtracker.iconset/icon_16x16.png
    sips -z 32 32     billtracker.png --out billtracker.iconset/icon_16x16@2x.png
    sips -z 32 32     billtracker.png --out billtracker.iconset/icon_32x32.png
    sips -z 64 64     billtracker.png --out billtracker.iconset/icon_32x32@2x.png
    sips -z 128 128   billtracker.png --out billtracker.iconset/icon_128x128.png
    sips -z 256 256   billtracker.png --out billtracker.iconset/icon_128x128@2x.png
    sips -z 256 256   billtracker.png --out billtracker.iconset/icon_256x256.png
    sips -z 512 512   billtracker.png --out billtracker.iconset/icon_256x256@2x.png
    sips -z 512 512   billtracker.png --out billtracker.iconset/icon_512x512.png
    cp billtracker.png billtracker.iconset/icon_512x512@2x.png
    iconutil -c icns billtracker.iconset
    rm -rf billtracker.iconset
fi

# Update spec file to use .icns on macOS
export ICON_FILE="billtracker.icns"

# Build with PyInstaller
pyinstaller Billtracker_qt.spec --clean --noconfirm

# Copy Info.plist to app bundle
if [ -f "Info.plist" ]; then
    cp Info.plist "${APP_BUNDLE}/Contents/Info.plist"
fi

# Copy icon to Resources
mkdir -p "${APP_BUNDLE}/Contents/Resources"
cp billtracker.icns "${APP_BUNDLE}/Contents/Resources/billtracker.icns"

echo "App bundle created: ${APP_BUNDLE}"

# Create DMG installer
echo "Creating DMG installer..."

DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"

# Use create-dmg if available, otherwise use hdiutil
if command -v create-dmg &> /dev/null; then
    create-dmg \
        --volname "${APP_NAME}" \
        --volicon "billtracker.icns" \
        --window-pos 200 120 \
        --window-size 600 400 \
        --icon-size 100 \
        --icon "Billtracker_qt.app" 175 190 \
        --hide-extension "Billtracker_qt.app" \
        --app-drop-link 425 190 \
        "${BUILD_DIR}/${DMG_NAME}" \
        "${APP_BUNDLE}"
else
    echo "create-dmg not found, using hdiutil..."
    hdiutil create -volname "${APP_NAME}" -srcfolder "${APP_BUNDLE}" -ov -format UDZO "${BUILD_DIR}/${DMG_NAME}"
fi

echo ""
echo "✅ Build complete!"
echo "  - App Bundle: ${APP_BUNDLE}"
echo "  - DMG:        ${BUILD_DIR}/${DMG_NAME}"
echo ""
echo "⚠️  Note: This app is NOT signed or notarized."
echo "   Users will need to right-click → Open to bypass Gatekeeper."
