#!/bin/bash
# build_rpm.sh
# Script to create an .rpm package for BillTracker
# Requires rpmbuild tool (rpm-tools or rpm-org on Arch, rpm on Debian/Ubuntu, rpm-build on Fedora/RHEL)

set -e  # Exit on error

VERSION="7.1.15"
APP_NAME="billtracker"
PKG_NAME="${APP_NAME}-${VERSION}-1.x86_64"
BUILD_ROOT="/tmp/billtracker_rpm_build"

echo "Building .rpm package for ${APP_NAME} v${VERSION}..."

# 0. Check for rpmbuild
if ! command -v rpmbuild &> /dev/null; then
    echo "Error: rpmbuild is not installed."
    echo "Please install it using your package manager:"
    echo "  Arch: sudo pacman -S rpm-tools"
    echo "  Debian/Ubuntu: sudo apt install rpm"
    echo "  Fedora/RHEL: sudo dnf install rpm-build"
    exit 1
fi

# 1. Ensure the executable is built
if [ ! -f "dist/Billtracker_qt" ]; then
    echo "Executable not found or rebuild needed."
    echo "Creating temporary build environment..."
    
    # Create a fresh venv for the build to avoid path issues in containers
    if [ -d "venv_rpm" ]; then
        rm -rf venv_rpm
    fi
    python3 -m venv venv_rpm
    
    # Install dependencies
    echo "Installing dependencies..."
    ./venv_rpm/bin/pip install -r requirements.txt
    ./venv_rpm/bin/pip install pyinstaller
    
    # Build with PyInstaller
    echo "Running PyInstaller..."
    ./venv_rpm/bin/pyinstaller Billtracker_qt.spec --clean --noconfirm
    
    # Cleanup venv (optional, but good to save space)
    # rm -rf venv_rpm
fi

# 2. Setup RPM build directory structure
echo "Setting up RPM build environment..."
rm -rf "${BUILD_ROOT}"
mkdir -p "${BUILD_ROOT}/BUILD"
mkdir -p "${BUILD_ROOT}/RPMS"
mkdir -p "${BUILD_ROOT}/SOURCES"
mkdir -p "${BUILD_ROOT}/SPECS"
mkdir -p "${BUILD_ROOT}/SRPMS"

# 3. Create spec file
echo "Creating spec file..."
cat > "${BUILD_ROOT}/SPECS/${APP_NAME}.spec" <<EOF
Name:           ${APP_NAME}
Version:        ${VERSION}
Release:        1%{?dist}
Summary:        Personal Finance Manager - Track bills and manage budgets
License:        Proprietary
URL:            https://github.com/grouvya/BillTracker
BuildArch:      x86_64

# Dependencies (adjust as needed)
Requires:       glibc
# Suggests:       python3-pyqt6

%description
BillTracker is a powerful and easy-to-use tool for tracking bills, 
managing budgets, and keeping your finances in order.

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/${APP_NAME}
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps

# Copy files
install -m 755 -D "${PWD}/dist/Billtracker_qt" %{buildroot}/usr/lib/${APP_NAME}/billtracker_qt
install -m 644 -D "${PWD}/billtracker.png" %{buildroot}/usr/share/icons/hicolor/256x256/apps/billtracker.png

# Create desktop file
cat > %{buildroot}/usr/share/applications/${APP_NAME}.desktop <<ENTRY
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
ENTRY

# Create symlink
ln -s /usr/lib/${APP_NAME}/billtracker_qt %{buildroot}/usr/bin/${APP_NAME}

%files
/usr/bin/${APP_NAME}
/usr/lib/${APP_NAME}/billtracker_qt
/usr/share/applications/${APP_NAME}.desktop
/usr/share/icons/hicolor/256x256/apps/billtracker.png

%post
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f -t /usr/share/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/gtk-update-icon-cache -f -t /usr/share/icons/hicolor &> /dev/null || :

%changelog
* $(date "+%a %b %d %Y") grouvya <grouvya@example.com> - ${VERSION}-1
- Automatic build
EOF

# 4. Build the package
echo "Running rpmbuild..."
rpmbuild -bb \
    --define "_topdir ${BUILD_ROOT}" \
    "${BUILD_ROOT}/SPECS/${APP_NAME}.spec"

# 5. Move output
# Find the generated rpm file (it might have dist tag like .fc38 or similar if configured, or just .x86_64)
GENERATED_RPM=$(find "${BUILD_ROOT}/RPMS" -name "*.rpm" | head -n 1)

if [ -f "$GENERATED_RPM" ]; then
    mv "$GENERATED_RPM" "./"
    FINAL_RPM_NAME=$(basename "$GENERATED_RPM")
    echo ""
    echo "✅ Package created: ${FINAL_RPM_NAME}"
    echo "To install: sudo rpm -i ${FINAL_RPM_NAME} (or use your package manager)"
else
    echo "❌ Error: RPM package was not created."
    exit 1
fi
