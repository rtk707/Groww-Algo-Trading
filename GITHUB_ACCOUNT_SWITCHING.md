# How to Switch Between GitHub Accounts

You have two GitHub accounts configured:

## Your Accounts:
1. **Personal Account** (`github.com-personal`) - Uses `id_rsa_personal`
2. **Work Account** (`github.com-work`) - Uses `id_ed25519`

## How to Use Work Account for a Repository:

### Method 1: Change Remote URL (Recommended)

For any repository where you want to use your **work account**:

```bash
cd /path/to/your/repo

# Change remote to use work account
git remote set-url origin git@github.com-work:username/repo-name.git

# Set git config for this repo
git config user.name "Your Work Name"
git config user.email "your-work-email@trajector.com"

# Verify
git remote -v
```

### Method 2: Clone New Repository with Work Account

```bash
# Clone using work account
git clone git@github.com-work:username/repo-name.git

cd repo-name

# Set git config
git config user.name "Your Work Name"
git config user.email "your-work-email@trajector.com"
```

## Current Repository Status:

**This repo (Groww-Algo-Trading)** is using:
- **Personal account** (`github.com-personal`)
- Remote: `git@github.com-personal:rtk707/Groww-Algo-Trading.git`

## Quick Reference:

**For Personal Account:**
```bash
git remote set-url origin git@github.com-personal:username/repo.git
git config user.name "rtk707"
git config user.email "your-personal-email@example.com"
```

**For Work Account:**
```bash
git remote set-url origin git@github.com-work:username/repo.git
git config user.name "Ritik Bansal"
git config user.email "ritik.bansal@trajector.com"
```

## Check Current Configuration:

```bash
# Check remote
git remote -v

# Check git config for current repo
git config user.name
git config user.email

# Check global git config
git config --global user.name
git config --global user.email
```

## Test SSH Connection:

```bash
# Test personal account
ssh -T git@github.com-personal

# Test work account
ssh -T git@github.com-work
```
