# GitHub Push Guide for Numbers.AI

This guide shows how to manually push any future changes to your Numbers.AI repository.

## Quick Reference Commands

### 1. Check Current Status
```bash
git status
```
Shows what files have been changed, added, or deleted.

### 2. Add All Changes
```bash
git add .
```
Adds all modified, new, and deleted files to the staging area.

### 3. Commit Changes
```bash
git commit -m "Your descriptive message here"
```
Example: `git commit -m "Add new stock analysis features and update reports"`

### 4. Push to GitHub
```bash
git push origin main
```

## Common Scenarios

### Scenario A: Simple Changes (most common)
```bash
git status
git add .
git commit -m "Describe your changes"
git push origin main
```

### Scenario B: If Push is Rejected (branch diverged)
```bash
git pull origin main
# Resolve any conflicts if they occur
git push origin main
```

### Scenario C: If Git Lock Error
```bash
# Remove lock file
del ".git\index.lock"
# Then try your commands again
```

### Scenario D: Selective File Changes
```bash
# Add specific files only
git add filename.py
git add README.md
git commit -m "Update specific files"
git push origin main
```

## Troubleshooting

### Error: "Updates were rejected"
**Solution**: Pull first, then push
```bash
git pull origin main
git push origin main
```

### Error: "Merge conflict"
**Solution**: 
1. Open conflicted files and resolve conflicts
2. Add resolved files: `git add .`
3. Commit: `git commit -m "Resolve merge conflicts"`
4. Push: `git push origin main`

### Error: "Unable to create index.lock"
**Solution**: Remove lock file
```bash
del ".git\index.lock"
```

### Error: "Authentication failed"
**Solution**: Check GitHub credentials or use GitHub CLI

## Best Practices

1. **Always check status first**: `git status` shows what will be committed
2. **Write descriptive commit messages**: Explain what changed and why
3. **Pull before pushing**: Avoid conflicts by pulling latest changes first
4. **Commit frequently**: Small, focused commits are easier to manage
5. **Check after push**: Verify changes appear on GitHub

## Example Workflow

```bash
# 1. Check what changed
git status

# 2. Add all changes
git add .

# 3. Commit with descriptive message
git commit -m "Update stock analysis algorithm and fix data processing bugs"

# 4. Push to GitHub
git push origin main

# 5. Verify success
git status  # Should show "working tree clean"
```

## What Gets Pushed?

- Modified Python files (`.py`)
- Updated documentation (`.md`)
- New reports in `reports/` folder
- Configuration changes
- Any other tracked files

## What Doesn't Get Pushed?

- Log files (`.log`) - typically in `.gitignore`
- Virtual environment folders
- Temporary files
- Files listed in `.gitignore`

---

**Remember**: Always make sure you're in the Numbers.AI directory before running these commands!
