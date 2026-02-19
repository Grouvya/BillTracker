# Flathub Submission Guide

Flathub is the central repository for Flatpak applications. Submitting your app involves a few steps on GitHub.

## Prerequisites
- A GitHub account.
- A built and tested Flatpak (which we are doing now).

## Steps

### 1. Fork the Flathub Repository
1. Go to [https://github.com/flathub/flathub](https://github.com/flathub/flathub).
2. Click the **Fork** button in the top right corner to create a copy of the repository in your own account.

### 2. Add Your Application
1. Clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/flathub.git
   cd flathub
   ```
2. Create a new branch for your app:
   ```bash
   git checkout -b new-app/org.grouvya.BillTracker
   ```
3. Create a directory named `org.grouvya.BillTracker`:
   ```bash
   mkdir org.grouvya.BillTracker
   ```
4. Copy the following files into this new directory:
   - `org.grouvya.BillTracker.json` (The manifest file)
   - `org.grouvya.BillTracker.metainfo.xml` (The AppStream metadata)
   - `org.grouvya.BillTracker.desktop` (The desktop entry)
   - Any icons (e.g., `billtracker_128.png`, `billtracker_512.png`)
   - `flathub.json` (Optional, if you need specific build options for Flathub, usually not needed initially)

   > **Note:** For Flathub, it's best if the source code is downloaded from a URL (like a tarball release on GitHub) rather than using local files. We might need to adjust the manifest to point to a release tag of your repository instead of local files.

### 3. Adjust Manifest for Remote Source
**Crucial Step:** Flathub builders cannot access your local files. You must update `org.grouvya.BillTracker.json` to pull the source code from your GitHub repository.

Change the `sources` section in `org.grouvya.BillTracker.json` to look something like this:
```json
"sources": [
    {
        "type": "git",
        "url": "https://github.com/grouvya/BillTracker.git",
        "tag": "v7.4.0",
        "commit": "YOUR_COMMIT_HASH_HERE"
    }
]
```
Alternatively, use a tarball release:
```json
"sources": [
    {
        "type": "archive",
        "url": "https://github.com/grouvya/BillTracker/archive/refs/tags/v7.4.0.tar.gz",
        "sha256": "SHA256_OF_THE_TARBALL"
    }
]
```

### 4. Commit and Push
1. Add the files:
   ```bash
   git add org.grouvya.BillTracker/
   ```
2. Commit your changes:
   ```bash
   git commit -m "Add org.grouvya.BillTracker"
   ```
3. Push to your fork:
   ```bash
   git push origin new-app/org.grouvya.BillTracker
   ```

### 5. Create a Pull Request
1. Go to your fork on GitHub.
2. You should see a prompt to create a Pull Request. Click "Compare & pull request".
3. Ensure the base repository is `flathub/flathub` and the base branch is `new-pr`.
4. Fill in the PR description.
5. Submit the Pull Request.

### 6. Review Process
- The Flathub bot will run automated checks.
- Maintainers will review your PR.
- You might need to make changes based on feedback.
- Once approved, your app will be merged and published!

## Maintenance
- When you release a new version, you'll create a new PR to update the manifest with the new tag/commit and updated metadata.
