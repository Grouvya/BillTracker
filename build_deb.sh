#!/bin/bash
# build_deb.sh
# Script to create a .deb package for BillTracker

set -e  # Exit on error

VERSION="7.1.15"
APP_NAME="billtracker"
PKG_NAME="${APP_NAME}_${VERSION}_amd64"
BUILD_DIR="/tmp/billtracker_deb_build"

echo "Building .deb package for ${APP_NAME} v${VERSION}..."

# 0. Clean up previous temp build
echo "Cleaning up temporary build directory..."
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# 1. Ensure the executable is built
if [ ! -f "dist/Billtracker_qt" ]; then
    echo "Executable not found. Running build_linux.sh..."
    bash build_linux.sh
fi

# 2. Setup directory structure
echo "Setting up directory structure..."
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}/${PKG_NAME}/DEBIAN"
mkdir -p "${BUILD_DIR}/${PKG_NAME}/usr/bin"
mkdir -p "${BUILD_DIR}/${PKG_NAME}/usr/lib/${APP_NAME}"
mkdir -p "${BUILD_DIR}/${PKG_NAME}/usr/share/applications"
mkdir -p "${BUILD_DIR}/${PKG_NAME}/usr/share/icons/hicolor/256x256/apps"

# 3. Copy files
echo "Copying files..."
cp "dist/Billtracker_qt" "${BUILD_DIR}/${PKG_NAME}/usr/lib/${APP_NAME}/billtracker_qt"
cp "billtracker.png" "${BUILD_DIR}/${PKG_NAME}/usr/share/icons/hicolor/256x256/apps/billtracker.png"

# Create a modified desktop file for the system installation
cat > "${BUILD_DIR}/${PKG_NAME}/usr/share/applications/billtracker.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=BillTracker
Comment=Personal Finance Manager - Track bills and manage budgets
Exec=${APP_NAME}
Icon=billtracker
Terminal=false
Categories=Office;Finance;Qt;
Keywords=finance;bills;budget;money;tracker;
StartupNotify=true
StartupWMClass=Billtracker_qt
EOF

# Create a symlink in /usr/bin
ln -s "/usr/lib/${APP_NAME}/billtracker_qt" "${BUILD_DIR}/${PKG_NAME}/usr/bin/${APP_NAME}"

# 4. Create control file
echo "Creating control file..."
chmod 755 "${BUILD_DIR}/${PKG_NAME}/DEBIAN"
cat > "${BUILD_DIR}/${PKG_NAME}/DEBIAN/control" <<EOF
Package: ${APP_NAME}
Version: ${VERSION}
Section: office
Priority: optional
Architecture: amd64
Maintainer: grouvya
Description: Personal Finance Manager - Track bills and manage budgets
 BillTracker is a powerful and easy-to-use tool for tracking bills, 
 managing budgets, and keeping your finances in order.
EOF

# 5. Create postinst script for desktop shortcut and cache updates
echo "Creating postinst script..."
cat > "${BUILD_DIR}/${PKG_NAME}/DEBIAN/postinst" <<'EOF'
#!/bin/bash
set -e

# Update icon cache
gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true

# Update desktop database
update-desktop-database /usr/share/applications || true

# Create desktop shortcut for the current user if possible
if [ -n "$SUDO_USER" ]; then
    USER_HOME=$(getent passwd "$SUDO_USER" | cut -d: -f6)
    DESKTOP_DIR="$USER_HOME/Desktop"
    if [ -d "$DESKTOP_DIR" ]; then
        cp /usr/share/applications/billtracker.desktop "$DESKTOP_DIR/"
        # Fix permissions
        chown "$SUDO_USER:$SUDO_USER" "$DESKTOP_DIR/billtracker.desktop"
        chmod +x "$DESKTOP_DIR/billtracker.desktop"
    fi
fi

exit 0
EOF

# 5.1 Create postrm script for cleanup
echo "Creating postrm script..."
cat > "${BUILD_DIR}/${PKG_NAME}/DEBIAN/postrm" <<'EOF'
#!/bin/bash
set -e

# Update icon cache
gtk-update-icon-cache -f -t /usr/share/icons/hicolor || true

# Update desktop database
update-desktop-database /usr/share/applications || true

# Remove desktop shortcut for all users if it exists
# (Since we don't know exactly which users had it, but we can try to find and remove it)
for user_home in /home/*; do
    if [ -d "$user_home/Desktop" ]; then
        rm -f "$user_home/Desktop/billtracker.desktop"
    fi
done

exit 0
EOF

chmod 755 "${BUILD_DIR}/${PKG_NAME}/DEBIAN/postinst"
chmod 755 "${BUILD_DIR}/${PKG_NAME}/DEBIAN/postrm"

# 6. Build the package
echo "Running dpkg-deb --build..."
dpkg-deb --build "${BUILD_DIR}/${PKG_NAME}"

# 7. Move output
mv "${BUILD_DIR}/${PKG_NAME}.deb" "./${PKG_NAME}.deb"

echo ""
echo "✅ Package created: ${PKG_NAME}.deb"
echo "To install: sudo dpkg -i ${PKG_NAME}.deb"
echo "To uninstall: sudo apt remove ${APP_NAME}"
