#!/bin/bash
set -e

# Check for flatpak-builder
if ! command -v flatpak-builder &> /dev/null; then
    echo "Error: flatpak-builder is not installed."
    echo "Please install it using: sudo apt install flatpak-builder"
    exit 1
fi

# Ensure Flathub remote exists
flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

# Download flatpak-pip-generator if not present
if [ ! -f "flatpak-pip-generator.py" ]; then
    echo "Downloading flatpak-pip-generator..."
    wget -O flatpak-pip-generator.py https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator.py
    chmod +x flatpak-pip-generator.py
fi

# Setup Python Env for generation
if [ ! -d "venv_linux" ]; then
    python3 -m venv venv_linux
fi
./venv_linux/bin/pip install "setuptools==65.7.0" requirements-parser maturin setuptools-rust wheel

# Generate Python dependencies
echo "Generating Python dependencies..."
./venv_linux/bin/python flatpak-pip-generator.py --requirements-file=requirements_flatpak.txt --output pypi-dependencies --ignore-installed setuptools

# Build the Flatpak
echo "Building Flatpak..."
mkdir -p build_dir
mkdir -p repo
flatpak-builder --force-clean --repo=repo --install --user --install-deps-from=flathub build_dir org.grouvya.BillTracker.json

echo "Build complete! installed to user installation."
echo "Run with: flatpak run org.grouvya.BillTracker"
