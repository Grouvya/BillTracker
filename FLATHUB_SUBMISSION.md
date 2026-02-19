# Submitting BillTracker to Flathub (Linux Mint App Store)

Linux Mint uses Flathub as its primary source for apps. To get BillTracker into the generic "Software Manager", you must submit it to Flathub.

## Prerequisites

1.  **GitHub Account**: Required for hosting code and submitting the Pull Request.
2.  **Git**: Installed on your local machine (`sudo apt install git`).
3.  **Flatpak Builder**: Already installed and verified.

---

## Step 1: Host Your Source Code on GitHub

Flathub builds applications from **source**, not from local files on your computer. You must push your code to a public GitHub repository.

1.  **Create a Repository**:
    *   Go to [GitHub](https://github.com/new) and create a repository named `BillTracker`.
    *   Make it **Public**.

2.  **Configure Git (First Time Only)**:
    If this is your first time using Git on this machine, run these commands:
    ```bash
    git config --global user.email "your_email@example.com"
    git config --global user.name "Your Name"
    ```

3.  **Push Your Code**:
    Run these commands in your project folder (`/media/grouvya/Archive HDD/Billtracker`):
    ```bash
    git init
    git add .
    git commit -m "Initial release of BillTracker"
    git branch -M main
    
    # If the remote 'origin' already exists, update it:
    git remote remove origin || true
    git remote add origin https://github.com/grouvya/BillTracker.git
    
    # When prompted for password, use a Personal Access Token (PAT)
    git push -u origin main
    ```

    **Important on Authentication:**
    GitHub requires a **Personal Access Token (PAT)** instead of your password.
    1.  Click this direct link: [Generate New Token (Classic)](https://github.com/settings/tokens/new)
    2.  **Note**: Ensure "Classic" is selected if prompted.
    3.  **Scopes**: Check the box for **`repo`** (Full control of private repositories).
    4.  Scroll down and click **Generate token**.
    5.  **Copy the token** (starts with `ghp_`).
    6.  When Git asks for your password, **paste this token**.

3.  **Create a Release Tag**:
    Flathub needs a specific "version" to build. Create a release for `v1.0.0` (or your current version):
    *   Go to your GitHub repo page.
    *   Click **Releases** > **Draft a new release**.
    *   Choose a tag: `v1.0.0`.
    *   Title: `BillTracker v1.0.0`.
    *   Click **Publish release**.

---

## Step 2: Update the Flatpak Manifest

Now that your code is online, you must tell the Flatpak builder where to find it.

1.  **Open `org.grouvya.BillTracker.json`**.
2.  **Locate the `sources` section** (currently pointing to local files like `"path": "Billtracker_qt.py"`).
3.  **Replace the `sources` block** with a reference to your GitHub release.

    **Replace this:**
    ```json
    "sources": [
        { "type": "file", "path": "Billtracker_qt.py" },
        ...
    ]
    ```

    **With this (update URL with your repo):**
    ```json
    "sources": [
        {
            "type": "archive",
            "url": "https://github.com/grouvya/BillTracker/archive/refs/tags/v1.0.0.tar.gz",
            "sha256": "GENERATED_HASH"
        }
    ]
    ```

    **How to get the SHA256 Hash:**
    Run this command on your terminal:
    ```bash
    curl -L https://github.com/grouvya/BillTracker/archive/refs/tags/v1.0.0.tar.gz | sha256sum
    ```
    Copy the long string output into the `"sha256"` field above.

---

## Step 3: Validate the New Manifest

Verify that your new manifest correctly pulls from GitHub and builds.

1.  Run the build command:
    ```bash
    flatpak-builder --force-clean --user --install --repo=repo build_dir org.grouvya.BillTracker.json
    ```
2.  If it builds successfully, you are ready to submit!

---

## Step 4: Submit to Flathub

**CRITICAL: You CANNOT upload directly to the main Flathub repository.**
If you see "Uploads are disabled", it means you missed step 1 below.

1.  **Fork the Repository (REQUIRED)**:
    *   Go to [https://github.com/flathub/flathub](https://github.com/flathub/flathub).
    *   Click the **Fork** button in the top-right corner.
    *   This creates a copy under **YOUR account** (e.g., `https://github.com/grouvya/flathub`).

2.  **Create a Branch on YOUR Fork**:
    *   Go to **YOUR** new fork: `https://github.com/grouvya/flathub`.
    *   Click the "main" branch dropdown -> type `org.grouvya.BillTracker` -> click **Create branch**.

3.  **Upload Files to YOUR Branch**:
    *   While on your new branch (`org.grouvya.BillTracker`), click **Add file** -> **Upload files**.
    *   Drag and drop the 4 files from the `flathub_submission` folder.
    *   Click **Commit changes**.

4.  **Create Pull Request**:
    *   After committing, you will see a banner: "This branch is 1 commit ahead of flathub:main".
    *   Click **Contribute** -> **Open pull request**.
    *   Title: "Add org.grouvya.BillTracker".
    *   Click **Create pull request**.

5.  **Wait for Review**:
    A bot will check your build. Once verified, a human reviewer will check your app logic and metadata.

6.  **Publish**:
    Once merged, your app will appear on Flathub and in the Linux Mint Software Manager within 24 hours!
