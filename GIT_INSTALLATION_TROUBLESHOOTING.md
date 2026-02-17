# Git Installation Troubleshooting

## Problem: "git is not recognized as a command"

This means Git is either:
1. Not installed properly
2. Not added to Windows PATH

## Solution 1: Verify Git Installation

### Step 1: Check if Git is installed
1. Open File Explorer
2. Check if Git is installed in one of these locations:
   - `C:\Program Files\Git`
   - `C:\Program Files (x86)\Git`
   - `C:\Users\YourUsername\AppData\Local\Programs\Git`

### Step 2: If Git folder exists, add to PATH manually

1. **Copy the Git path** (example: `C:\Program Files\Git\cmd`)
2. **Open System Environment Variables**:
   - Press `Windows + R`
   - Type: `sysdm.cpl`
   - Press Enter
3. Click **"Environment Variables"** button
4. Under **"System variables"**, find and select **"Path"**
5. Click **"Edit"**
6. Click **"New"**
7. Paste: `C:\Program Files\Git\cmd`
8. Click **"New"** again
9. Paste: `C:\Program Files\Git\bin`
10. Click **"OK"** on all windows
11. **Restart your computer** (important!)

## Solution 2: Reinstall Git Properly

### Download and Install:
1. Go to: https://git-scm.com/download/win
2. Download the latest version (64-bit recommended)
3. Run the installer
4. **IMPORTANT**: During installation, make sure these options are selected:
   - ✅ "Git from the command line and also from 3rd-party software"
   - ✅ "Use Windows' default console window"
5. Complete the installation
6. **Restart your computer**

## Solution 3: Use Git Bash Instead

If you can't get Git working in PowerShell:

1. Find **"Git Bash"** in your Start Menu
2. Open Git Bash
3. Navigate to your project:
   ```bash
   cd "/c/Users/sakshi/Downloads/micro project"
   ```
4. Run Git commands there

## After Installation - Test Git:

Open a **NEW** PowerShell window and run:
```powershell
git --version
```

You should see something like: `git version 2.43.0.windows.1`

## Quick Setup Commands (After Git Works):

```bash
# Configure Git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: KindPlate Food Donation Platform"
```

## Alternative: Use GitHub Desktop

If command-line Git is too complicated:

1. Download GitHub Desktop: https://desktop.github.com/
2. Install it
3. Open GitHub Desktop
4. Click "Add" → "Add Existing Repository"
5. Select your project folder
6. Use the GUI to commit and push

## Need Help?

If none of these work, you can:
1. Use GitHub Desktop (easier GUI)
2. Use VS Code's built-in Git (if you have VS Code)
3. Ask for help with the specific error message you're seeing
