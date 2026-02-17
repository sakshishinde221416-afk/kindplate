# Git Setup Instructions

## Step 1: Install Git

### For Windows:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings (recommended)
4. Restart your terminal/command prompt

### For macOS:
```bash
brew install git
```

### For Linux:
```bash
sudo apt-get install git  # Ubuntu/Debian
sudo yum install git      # CentOS/RHEL
```

## Step 2: Configure Git (First Time Setup)

After installing Git, configure your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 3: Initialize Git Repository

Navigate to your project folder and run:

```bash
# Initialize git repository
git init

# Add all files to staging
git add .

# Create first commit
git commit -m "Initial commit: KindPlate Food Donation Platform"
```

## Step 4: Connect to GitHub (Optional)

If you want to push to GitHub:

1. Create a new repository on GitHub (https://github.com/new)
2. Don't initialize with README, .gitignore, or license
3. Run these commands:

```bash
git remote add origin https://github.com/yourusername/kindplate.git
git branch -M main
git push -u origin main
```

## What's Already Done:

✅ `.gitignore` file created - This tells Git which files to ignore
   - Python cache files (__pycache__, *.pyc)
   - Virtual environments (venv/, env/)
   - Database files (*.sqlite3)
   - Media files (uploaded images)
   - IDE settings (.vscode/, .idea/)
   - Environment variables (.env)

## Useful Git Commands:

```bash
# Check status
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# View commit history
git log

# Create a new branch
git branch feature-name

# Switch to a branch
git checkout feature-name

# Push to remote
git push origin main
```

## Project Structure (What Will Be Committed):

```
kindplate/
├── donations/              # Main Django app
├── food_donation_project/  # Django settings
├── static/                 # CSS, JS files
├── manage.py              # Django management
└── .gitignore             # Git ignore rules
```

## What Will Be Ignored:

- `media/` - User uploaded images (too large for git)
- `__pycache__/` - Python cache files
- `.vscode/` - Editor settings
- `*.pyc` - Compiled Python files
- Database files

## Note:

The `.gitignore` file is already created and configured for Django projects.
Once you install Git, you can run the commands in Step 3 to start version control.
