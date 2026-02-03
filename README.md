# 💰 BillTracker - Personal Finance Manager

**Version 5.5.0 Cross-Platform** | Created by **Grouvya**

A modern, secure cross-platform application for tracking bills, managing budgets, and monitoring your financial health. Available for **Windows**, **macOS**, and **Linux**.


---

## ✨ Features

### 📊 Financial Management
- **Bill Tracking**: Manage unpaid and paid bills with due dates
- **Budget Management**: Set and monitor your monthly budget
- **Multi-Currency Support**: Track expenses in different currencies with real-time exchange rates
- **Category Organization**: Organize bills by categories (Utilities, Rent, Subscriptions, etc.)
- **Recurring Bills**: Automatically create weekly, monthly, or yearly recurring bills

### 📈 Visualization & Analytics
- **Dashboard**: Quick overview of your financial status
- **Charts**: Visual breakdown of budget vs expenses and spending by category
- **Trends**: Monthly spending history with bar charts
- **Calendar View**: Visual representation of bill due dates

### 🔔 Smart Notifications
- **Due Date Reminders**: Get notified about upcoming bills
- **Background Monitoring**: App runs in system tray and checks every 4 hours
- **Startup Notifications**: See bills due today when you start your computer

### 🔒 Security & Data Protection
- **SHA-256 Hash Verification**: Ensures data integrity
- **Atomic File Writes**: Prevents data corruption
- **Path Validation**: Protects against malicious file operations
- **Input Sanitization**: Prevents injection attacks
- **Automatic Backups**: Regular backups of your financial data

### 🎨 Modern Interface
- **Dark/Light Themes**: Automatic theme switching based on system preferences
- **Smooth Animations**: Polished user experience with loading screens
- **Responsive Design**: Clean, modern PyQt6 interface
- **System Tray Integration**: Minimize to tray for background operation

---

## 🚀 Quick Start

### Installation

#### Windows
1. Download `Billtracker_qt_Installer.exe` from the [latest release](../../releases/latest)
2. Run the installer (requires Administrator privileges)
3. Launch BillTracker from Start Menu or Desktop shortcut

#### macOS
1. Download `BillTracker-5.5.0-macOS.dmg` from the [latest release](../../releases/latest)
2. Open the DMG file
3. Drag **BillTracker** to your Applications folder
4. **First launch**: Right-click the app → **Open** (required for unsigned apps)
5. Click **Open** in the security dialog

#### Linux
**Option 1: AppImage (Recommended)**
1. Download `BillTracker-5.5.0-x86_64.AppImage` from the [latest release](../../releases/latest)
2. Make it executable:
   ```bash
   chmod +x BillTracker-5.5.0-x86_64.AppImage
   ```
3. Run it:
   ```bash
   ./BillTracker-5.5.0-x86_64.AppImage
   ```

**Option 2: Tarball**
1. Download `BillTracker-5.5.0-linux-x86_64.tar.gz` from the [latest release](../../releases/latest)
2. Extract and run:
   ```bash
   tar -xzf BillTracker-5.5.0-linux-x86_64.tar.gz
   ./Billtracker_qt
   ```

### First Time Setup
1. **Set Your Budget**: Enter your monthly budget in the Dashboard
2. **Add Bills**: Click "Add Bill" to create your first bill entry
3. **Configure Settings**: 
   - Enable "Start with Windows/macOS/Linux" for automatic startup
   - Enable "Minimize to Tray" to keep app running in background
4. **Choose Currency**: Select your preferred currency for budget and bills


---

## 📖 User Guide

### Adding a Bill
1. Click **"Add Bill"** button
2. Fill in bill details:
   - Name (e.g., "Electric Bill")
   - Amount
   - Currency
   - Due Date
   - Category
   - Recurrence (optional)
3. Click **"Add"**

### Marking Bills as Paid
1. Select a bill from the Unpaid Bills list
2. Click **"Mark as Paid"**
3. Bill moves to Paid Bills tab automatically
4. If recurring, next bill is created automatically

### Viewing Analytics
- **Charts Tab**: See budget breakdown and category spending
- **Trends Tab**: View 6-month spending history
- **Calendar Tab**: Visual due date calendar with bill indicators

### Managing Data
- **Export**: Export bills to CSV for external analysis
- **Backup**: Automatic backups created on every save
- **Settings**: Configure data file location (must be in user directory)

---

## 🛡️ Security Features

### Data Protection
- All data files are validated with SHA-256 checksums
- Atomic writes prevent corruption during save operations
- Automatic backup system maintains data history
- **10MB file size limit** to prevent DoS attacks

### Input Validation
- File paths restricted to user directories only
- Input sanitization prevents control character injection
- Maximum length limits on all text inputs

### Network Security
- SSL/TLS encryption for API calls
- Fallback API endpoints for reliability
- Timeout protection on network requests

### Error Logging
- Comprehensive logging system at `~/.bill_tracker/app.log`
- Tracks warnings and errors for debugging
- Specific exception handling with detailed error messages

---

## ⚙️ System Requirements

### Windows
- **OS**: Windows 10 or later
- **RAM**: 256 MB minimum
- **Disk Space**: 50 MB
- **Internet**: Optional (for exchange rate updates)

### macOS
- **OS**: macOS 11 (Big Sur) or later
- **RAM**: 256 MB minimum
- **Disk Space**: 50 MB
- **Internet**: Optional (for exchange rate updates)

### Linux
- **OS**: Ubuntu 22.04+, Fedora 38+, or equivalent
- **RAM**: 256 MB minimum
- **Disk Space**: 50 MB
- **Internet**: Optional (for exchange rate updates)

---

## 🛠️ Building from Source

Want to build the app yourself? Here's how to compile BillTracker on your system:

### Prerequisites (All Platforms)
- **Python 3.11+**
- **Git** (to clone the repository)

### Windows Build

```powershell
# Clone the repository
git clone https://github.com/Grouvya/billtracker.git
cd billtracker

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller Billtracker_qt.spec --clean --noconfirm

# Executable will be in: dist\Billtracker_qt.exe
```

**Optional: Create installer**
```powershell
# Install NSIS (if not already installed)
choco install nsis -y

# Build installer
makensis Billtracker_qt_installer.nsi

# Installer will be: Billtracker_qt_Installer.exe
```

### macOS Build

```bash
# Clone the repository
git clone https://github.com/Grouvya/billtracker.git
cd billtracker

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Install DMG creation tool
brew install create-dmg

# Make build script executable and run it
chmod +x build_macos.sh
./build_macos.sh

# App bundle: dist/Billtracker_qt.app
# DMG installer: dist/BillTracker-5.5.0-macOS.dmg
```

### Linux Build

```bash
# Clone the repository
git clone https://github.com/Grouvya/billtracker.git
cd billtracker

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y libxcb-xinerama0 libxcb-cursor0 libxkbcommon-x11-0 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 fuse libfuse2

# Install Python dependencies
pip install -r requirements.txt
pip install pyinstaller

# Make build script executable and run it
chmod +x build_linux.sh
./build_linux.sh

# AppImage: dist/BillTracker-5.5.0-x86_64.AppImage
# Tarball: dist/BillTracker-5.5.0-linux-x86_64.tar.gz
```

**For other Linux distributions:**
- **Fedora/RHEL**: Replace `apt-get` with `dnf` or `yum`
- **Arch**: Replace `apt-get` with `pacman`

### Running Without Building

If you just want to run the app without creating an installer:

```bash
# After installing dependencies
python Billtracker_qt.py
```

---

## 🔧 Technical Details

### Built With
- **Python 3.11**
- **PyQt6** - Modern GUI framework
- **Exchange Rate APIs** - Real-time currency conversion

### Data Storage
- JSON format for easy portability
- Located in user's AppData directory by default
- Configurable storage location

### Architecture
- Single-file executable (PyInstaller)
- No external dependencies required
- Portable installation option

---

## 📝 Version History

### v5.5.0 Cross-Platform (Current)
- 🌍 **macOS Support**: Full compatibility with macOS 11+
- 🐧 **Linux Support**: Full compatibility with Ubuntu, Fedora, and other distros
- 🚀 **Cross-Platform Startup**: Start on boot works on Windows, macOS, and Linux
- 🎨 **Platform Icons**: Automatic icon format selection (.ico for Windows, .png for Mac/Linux)
- 📦 **Build Scripts**: Included build scripts for all platforms

### v5.4.1 UX
- 🎨 **New Tray Icon**: Modern purple icon with dollar sign
- 🐛 **Fixed Quit Button**: Tray menu quit now properly terminates app
- ✨ **Close Dialog**: Ask user to quit or minimize when closing window
- 🎯 **Better UX**: Full control over app close behavior

### v5.4.0 Hardened
- 🔒 **Security Hardening**: Comprehensive logging system for debugging
- 🔒 **Enhanced Exception Handling**: Specific exception types with error logging
- 🔒 **File Size Validation**: 10MB limit to prevent DoS attacks
- 🐛 **Bug Fixes**: Removed 3 duplicate code blocks in initialization
- ⚡ **Performance**: Lazy loading for README (~50ms faster startup)
- ⚡ **Performance**: Chart caching (~100ms faster currency switching)
- 📊 **Total Improvement**: ~150ms+ faster overall performance

### v5.3.1 About
- 📚 Comprehensive README documentation
- ℹ️ New About tab displaying README in-app
- 📖 User guide, troubleshooting, and feature documentation

### v5.3.0 Security
- 🔒 Enhanced security with input sanitization
- 🔒 Path validation to prevent traversal attacks
- 🎨 Modern loading screen with progress indicators
- ✨ Improved error handling for registry operations

### v5.2.x Hotfixes
- 🐛 Fixed Trends tab crash (missing QRect import)
- 🐛 Fixed Calendar widget crash (missing QCalendarWidget import)
- 🛡️ Added admin privilege check to installer

### v5.2.0 Systems
- 📉 Minimize to tray functionality
- 🚀 Start with Windows option
- 🔔 Background payment reminders (every 4 hours)

### v5.1.0 Visuals
- 📅 Calendar tab with visual due dates
- 📊 Trends tab with spending history
- 🎨 Modern dark/light theme support

### v5.0.0 Pro
- 💝 "Created by Grouvya" branding
- 💰 Donate/Support button
- 📤 CSV export functionality
- 🔄 Recurring bills feature
- 🔐 Data integrity verification

---

## 💝 Support the Developer

If you find BillTracker useful, consider supporting the developer:

**Created with ❤️ by Grouvya**

Your support helps maintain and improve this free application!

---

## 📄 License

This software is provided as-is for personal use. All rights reserved.

---

## 🐛 Troubleshooting

### App won't start (Windows)
- Ensure you have Windows 10 or later
- Try running as Administrator
- Check Windows Defender hasn't quarantined the file

### App won't start (macOS)
- Right-click the app → **Open** (don't double-click)
- Go to System Settings → Privacy & Security → Allow app to run
- Ensure you have macOS 11 (Big Sur) or later

### App won't start (Linux)
- Make sure the AppImage is executable: `chmod +x BillTracker-*.AppImage`
- Install FUSE if needed: `sudo apt install fuse libfuse2` (Ubuntu/Debian)
- Try the tarball version if AppImage doesn't work

### Exchange rates not updating
- Check your internet connection
- The app uses fallback APIs if primary fails
- Rates update automatically on startup

### Data file issues
- Check file permissions in Settings
- Ensure path is in your user directory
- Restore from automatic backup if needed

### System tray not working
- Enable "Minimize to Tray" in Settings
- Check system notification area settings
- Restart the application


---

## 📧 Contact

For issues, suggestions, or feedback, please contact the developer through the app's "Support" button.

**Thank you for using BillTracker!** 🎉
