# Setting Up GitHub Repository

## Issue
The GH_TOKEN environment variable is set but invalid, preventing GitHub CLI from using the valid keyring token.

## Solution Options

### Option 1: Clear GH_TOKEN and Use GitHub CLI (Recommended)

In your terminal, run:
```bash
unset GH_TOKEN
cd ~/network-observability-platform
gh auth switch --user kmransom56
gh repo create network-observability-platform --public --source=. --remote=origin --description "A comprehensive network observability and management platform for enterprise network infrastructure"
git push -u origin main
```

### Option 2: Create Repository Manually on GitHub

1. Go to: https://github.com/new
2. Repository name: `network-observability-platform`
3. Description: "A comprehensive network observability and management platform for enterprise network infrastructure"
4. Set to **Public**
5. **DO NOT** initialize with README, .gitignore, or license (we already have them)
6. Click "Create repository"
7. Then run:
```bash
cd ~/network-observability-platform
git remote add origin https://github.com/kmransom56/network-observability-platform.git
git push -u origin main
```

### Option 3: Remove GH_TOKEN from Shell Profile

If GH_TOKEN is set in your `.zshrc` or `.bashrc`, remove or comment it out:
```bash
# Edit your shell profile
nano ~/.zshrc  # or ~/.bashrc

# Find and remove/comment the line:
# export GH_TOKEN=...

# Then reload:
source ~/.zshrc
```

Then use Option 1.
