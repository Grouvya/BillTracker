#!/bin/bash
set -e

# Configuration
APP_ID="org.grouvya.BillTracker"
SUBMISSION_DIR="flathub_submission"
MANIFEST="$SUBMISSION_DIR/$APP_ID.json"
TAG="v1.0.0"

echo "=========================================="
echo "    BillTracker Flathub Submission Helper"
echo "=========================================="
echo ""

# 1. Prerequisite Checks
echo "--- Step 1: Checks ---"
read -p "Have you forked 'https://github.com/flathub/flathub' to your account? [y/N] " FORKED
if [[ "$FORKED" != "y" && "$FORKED" != "Y" ]]; then
    echo "Please fork the repository first: https://github.com/flathub/flathub"
    exit 1
fi

read -p "Have you created Release '$TAG' on your BillTracker GitHub repo? [y/N] " RELEASED
if [[ "$RELEASED" != "y" && "$RELEASED" != "Y" ]]; then
    echo "Please create a release tagged '$TAG' on GitHub first."
    exit 1
fi

read -p "Enter your GitHub Username: " USERNAME
if [ -z "$USERNAME" ]; then
    echo "Username required."
    exit 1
fi

# 2. Verify Release and Get Hash
echo ""
echo "--- Step 2: verifying Release ---"
TARBALL_URL="https://github.com/$USERNAME/BillTracker/archive/refs/tags/$TAG.tar.gz"
echo "Checking URL: $TARBALL_URL"

if ! curl --output /dev/null --silent --head --fail "$TARBALL_URL"; then
    echo "Error: Could not access the release URL. Please check if the tag '$TAG' matches your release."
    exit 1
fi

echo "Calculating SHA256 hash (downloading...)"
SHA256=$(curl -L --silent "$TARBALL_URL" | sha256sum | awk '{print $1}')
echo "Hash: $SHA256"

# 3. Update Manifest
echo ""
echo "--- Step 3: Updating Manifest ---"
# We use Python for reliable JSON editing
./venv_linux/bin/python3 -c "
import json
import sys

manifest_path = '$MANIFEST'
tarball_url = '$TARBALL_URL'
sha256 = '$SHA256'

with open(manifest_path, 'r') as f:
    data = json.load(f)

# Find sources list
sources = data.get('modules', [])[-1].get('sources', [])

# Remove local python file source if present
sources = [s for s in sources if s.get('path') != 'Billtracker_qt.py']

# Remove existing archive source if present
sources = [s for s in sources if s.get('type') != 'archive']

# Add new archive source at the top
new_source = {
    'type': 'archive',
    'url': tarball_url,
    'sha256': sha256
}
sources.insert(0, new_source)

# Update manifest
data['modules'][-1]['sources'] = sources

with open(manifest_path, 'w') as f:
    json.dump(data, f, indent=4)
"

echo "Manifest updated successfully."

# 4. Clone and Push
echo ""
echo "--- Step 4: Pushing to Flathub Fork ---"
REPO_URL="https://github.com/$USERNAME/flathub.git"
CLONE_DIR="flathub_submission_repo"

rm -rf "$CLONE_DIR"
echo "Cloning $REPO_URL..."
git clone "$REPO_URL" "$CLONE_DIR"

cd "$CLONE_DIR"
BRANCH_NAME="$APP_ID"

echo "Creating branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME" || git checkout "$BRANCH_NAME"

echo "Copying files..."
cp "../$SUBMISSION_DIR/"* .

echo "Committing..."
git add "$APP_ID.json" pypi-dependencies.json "$APP_ID.desktop" billtracker_512.png
git commit -m "Add $APP_ID" || echo "Nothing to commit"

echo ""
echo "Pushing... (You may need to enter your GitHub credentials/PAT)"
git push -u origin "$BRANCH_NAME"

echo ""
echo "=========================================="
echo "SUCCESS!"
echo "Go here to open your Pull Request:"
echo "https://github.com/flathub/flathub/compare/master...$USERNAME:$BRANCH_NAME"
echo "=========================================="
