#!/bin/bash
# Linux Build Script for BillTracker

set -e  # Exit on error

VERSION="5.5.0"
APP_NAME="BillTracker"
BUILD_DIR="dist"
APPDIR="${BUILD_DIR}/${APP_NAME}.AppDir"

echo "Building ${APP_NAME} for Linux..."

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build with PyInstaller
pyinstaller Billtracker_qt.spec --clean --noconfirm

echo "Build complete! Executable is in ${BUILD_DIR}/Billtracker_qt"

# Create AppImage structure
echo "Creating AppImage..."
mkdir -p "${APPDIR}/usr/bin"
mkdir -p "${APPDIR}/usr/share/applications"
mkdir -p "${APPDIR}/usr/share/icons/hicolor/256x256/apps"

# Copy executable
cp "${BUILD_DIR}/Billtracker_qt" "${APPDIR}/usr/bin/billtracker_qt"

# Copy icon
cp billtracker.png "${APPDIR}/usr/share/icons/hicolor/256x256/apps/billtracker.png"
cp billtracker.png "${APPDIR}/billtracker.png"

# Copy desktop file
cp billtracker.desktop "${APPDIR}/usr/share/applications/billtracker.desktop"
cp billtracker.desktop "${APPDIR}/billtracker.desktop"

# Create AppRun script
cat > "${APPDIR}/AppRun" << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/billtracker_qt" "$@"
EOF

chmod +x "${APPDIR}/AppRun"

# Download appimagetool if not present
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

# Create AppImage
ARCH=x86_64 ./appimagetool-x86_64.AppImage "${APPDIR}" "${BUILD_DIR}/${APP_NAME}-${VERSION}-x86_64.AppImage"

echo "AppImage created: ${BUILD_DIR}/${APP_NAME}-${VERSION}-x86_64.AppImage"

# Create tarball as fallback
echo "Creating tarball..."
cd "${BUILD_DIR}"
tar -czf "${APP_NAME}-${VERSION}-linux-x86_64.tar.gz" Billtracker_qt
cd ..

echo ""
echo "✅ Build complete!"
echo "  - AppImage: ${BUILD_DIR}/${APP_NAME}-${VERSION}-x86_64.AppImage"
echo "  - Tarball:  ${BUILD_DIR}/${APP_NAME}-${VERSION}-linux-x86_64.tar.gz"
echo ""
echo "To run the AppImage:"
echo "  chmod +x ${BUILD_DIR}/${APP_NAME}-${VERSION}-x86_64.AppImage"
echo "  ./${BUILD_DIR}/${APP_NAME}-${VERSION}-x86_64.AppImage"
