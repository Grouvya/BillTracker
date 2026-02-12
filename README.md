# 💰 BillTracker - The Premium Financial Hub

Created with ❤️ by **Grouvya**

A modern, high-performance financial management ecosystem. Streamline your bills, automate your subscriptions, and crush your savings goals—all from a single, secure, and beautiful interface.

---

## 💎 Core Experience

### 📊 The Financial Command Center
- **Unified 360° Dashboard**: Instant clarity on your budget, upcoming bills, and savings milestones.
- **Smart Subscription Engine**: Identify "burn rate" patterns and manage recurring costs with surgical precision.
- **Savings Ecosystem**: Set targets, visualize progress with interactive charts, and reach your goals faster.
- **Advanced Global Search**: Lightning-fast (Ctrl+F) engine to find any transaction across categories, dates, or amounts.

### 🛡️ Iron-Clad Security
- **AES-256 Military-Grade Encryption**: Your data is protected by industry-standard Fernet architecture.
- **Secure PIN Access**: 4-6 digit biometric-inspired protection with brute-force lockout.
- **Auto-Lock Intelligence**: Customizable idle timeouts and "lock-on-minimize" to keep your data private.
- **Atomic Data Integrity**: Fail-safe save mechanisms and SHA-256 checksum verification.

---

## 📥 Installation & Compilation

BillTracker is built with Python 3 and Qt (PySide6/PyQt6). You can run it from source on any platform or compile it into a standalone executable.

### 🐧 Linux (Mint, Ubuntu, Debian)

**Option 1: Automated Script (Recommended)**
We provide a dedicated script for Debian-based systems that handles dependencies, virtual environments, and compilation.

1.  Open a terminal in the project directory.
2.  Run the compile script:
    ```bash
    chmod +x mint_compile.sh
    ./mint_compile.sh
    ```
    This will create a standalone executable in the `dist` folder.

**Option 2: Manual Install**
```bash
# Install system dependencies (Ubuntu/Mint)
sudo apt install python3-pip python3-venv libxcb-cursor0

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run the app
python3 Billtracker_qt.py
```

### 🪟 Windows

**Option 1: Build Installer (Requires NSIS)**
If you want to build the `.exe` installer yourself:
1.  Ensure Python 3.10+ is installed and added to PATH.
2.  Install [NSIS](https://nsis.sourceforge.io/Download).
3.  Double-click `build_installer_qt.bat`.
    - This script uses `PyInstaller` to build the generic executable.
    - It then runs `makensis` to generate `Billtracker_qt_Installer.exe`.

**Option 2: Manual Run**
```powershell
# Open Command Prompt/PowerShell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python Billtracker_qt.py
```

### 🍎 macOS

**Option 1: Build App Bundle**
1.  Open a terminal in the project directory.
2.  Run the build script:
    ```bash
    chmod +x build_macos.sh
    ./build_macos.sh
    ```
    - This will generate `dist/Billtracker_qt.app`.
    - It may also attempt to create a `.dmg` image if `create-dmg` is installed.

**Option 2: Manual Run**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 Billtracker_qt.py
```

---

## 🚀 Recent Updates (v7.1.14)
- **Top 5 Currencies**: Dynamic suggestions based on your bill and savings goal usage.
- **Donate Option**: Added easy access to Revolut donations in the About section.
- **Contact Update**: Direct Telegram support integration.
- **Persistence**: Fixed currency preference restoration for encrypted storage.

---

## 📧 Support & Community
Dedicated to providing the best personal finance tool. For feedback, feature requests, or support, use the **📩 Contact** button inside the app's About tab.

**Thank you for choosing BillTracker!** 🎉

