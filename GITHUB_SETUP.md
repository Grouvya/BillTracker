# GitHub Repository Setup Guide

## ✅ Git Installation Complete

Git has been successfully installed (version 2.52.0). However, you need to **restart your PowerShell terminal** for the PATH changes to take effect.

---

## 🚀 Quick Setup Steps

### Step 1: Restart PowerShell

**Close your current PowerShell window and open a new one.** This is required for Git to be recognized.

---

### Step 2: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `BillTracker` (or your preferred name)
   - **Description**: "Personal Finance Manager - Track bills and budgets"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**
5. **Copy the repository URL** (it will look like `https://github.com/YourUsername/BillTracker.git`)

---

### Step 3: Initialize Local Repository

Open a **new PowerShell window** in your project directory and run these commands:

```powershell
# Navigate to your project
cd "c:\Users\Grouv\OneDrive\Desktop\AntiGravity"

# Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Add GitHub Actions CI/CD for multi-platform builds"

# Rename branch to main (if needed)
git branch -M main

# Add remote (replace with YOUR repository URL from Step 2)
git remote add origin https://github.com/YourUsername/BillTracker.git

# Push to GitHub
git push -u origin main
```

---

### Step 4: Create a Release

Once pushed, create your first release to trigger the build workflow:

**Option A: Via GitHub Web UI**
1. Go to your repository on GitHub
2. Click **"Releases"** → **"Create a new release"**
3. Click **"Choose a tag"** → Type `v5.5.0` → Click **"Create new tag: v5.5.0 on publish"**
4. **Release title**: `BillTracker v5.5.0 - Multi-Platform Release`
5. **Description**: 
   ```markdown
   ## 🎉 First Multi-Platform Release
   
   Automated builds for Windows, macOS, and Linux!
   
   ### Downloads
   - **Windows**: `Billtracker_qt_Installer.exe`
   - **macOS**: `BillTracker-5.5.0-macOS.dmg`
   - **Linux**: `BillTracker-5.5.0-x86_64.AppImage`
   
   See README for installation instructions.
   ```
6. Click **"Publish release"**

**Option B: Via Command Line**
```powershell
git tag v5.9.0
git push origin v5.9.0
```

---

### Step 5: Watch the Magic! ✨

1. Go to your repository → **"Actions"** tab
2. You'll see the **"Build Multi-Platform Release"** workflow running
3. Watch as it builds all three installers in parallel (~15-20 minutes)
4. Once complete, go to **"Releases"** and you'll see all installers attached!

---

## 🔧 Troubleshooting

### Git still not recognized after restart
If Git is still not found after restarting PowerShell, manually add it to PATH:
```powershell
$env:Path += ";C:\Program Files\Git\cmd"
```

### Authentication issues when pushing
GitHub requires a Personal Access Token (PAT) instead of password:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use the token as your password when prompted

**Or use GitHub CLI for easier authentication:**
```powershell
winget install --id GitHub.cli
gh auth login
```

### OneDrive sync conflicts
Since your project is in OneDrive, you might see sync issues. Consider moving the repository to a non-synced location:
```powershell
# Move to a better location
Move-Item "c:\Users\Grouv\OneDrive\Desktop\AntiGravity" "c:\Users\Grouv\Projects\BillTracker"
cd "c:\Users\Grouv\Projects\BillTracker"
```

---

## 📝 Important Notes

### .gitignore File

Before committing, you should create a `.gitignore` file to exclude build artifacts:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/

# PyInstaller
build/
dist/
*.spec

# Installers
*.exe
*.dmg
*.AppImage
*.tar.gz
appimagetool-x86_64.AppImage

# macOS
.DS_Store
*.icns
billtracker.iconset/

# Linux
*.AppDir/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
```

Save this as `.gitignore` in your project root **before** running `git add .`

---

## ✅ Next Steps After Push

1. **Monitor GitHub Actions**: Watch your first build complete
2. **Test installers**: Download and test each platform's installer
3. **Update README**: Add build status badge (optional)
4. **Share**: Your app is now ready for distribution!

---

## 🎊 Summary

You now have:
- ✅ Git installed and configured
- ✅ GitHub Actions workflow ready
- ✅ Multi-platform build scripts
- ✅ Professional installers for Windows, macOS, and Linux

**Just restart PowerShell and follow the steps above!**
