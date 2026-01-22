# Setting Up Multiple GitHub Accounts on Same Device

## Method 1: SSH Keys (Recommended)

### Step 1: Generate SSH Key for Secondary Account

```bash
# Generate a new SSH key with a different name
ssh-keygen -t ed25519 -C "your-secondary-email@example.com" -f ~/.ssh/id_ed25519_secondary

# Or if ed25519 is not available:
ssh-keygen -t rsa -b 4096 -C "your-secondary-email@example.com" -f ~/.ssh/id_rsa_secondary
```

### Step 2: Add SSH Key to SSH Config

Edit `~/.ssh/config` file:

```bash
nano ~/.ssh/config
```

Add this configuration:

```
# Primary GitHub account
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# Secondary GitHub account
Host github-secondary
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_secondary
    IdentitiesOnly yes
```

### Step 3: Add SSH Key to GitHub

```bash
# Copy the public key
cat ~/.ssh/id_ed25519_secondary.pub
# Or
pbcopy < ~/.ssh/id_ed25519_secondary.pub
```

Then:
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste the key and save

### Step 4: Update Git Remote for This Repository

```bash
cd /Users/ritik.bansal/Downloads/groww_algo_trading_repo
git remote set-url origin git@github-secondary:rtk707/Groww-Algo-Trading.git
```

### Step 5: Test SSH Connection

```bash
ssh -T git@github-secondary
```

## Method 2: Git Config Per Repository

### Set Git Config for This Repository Only

```bash
cd /Users/ritik.bansal/Downloads/groww_algo_trading_repo
git config user.name "Your Secondary Account Name"
git config user.email "your-secondary-email@example.com"
```

### Use HTTPS with Credential Helper

```bash
# Set up credential helper
git config credential.helper store

# Or use cache (temporary)
git config credential.helper cache
```

## Method 3: GitHub CLI with Multiple Accounts

```bash
# Login with secondary account
gh auth login --hostname github.com

# Switch between accounts
gh auth switch
```

## Quick Setup for This Repository

Run these commands:

```bash
cd /Users/ritik.bansal/Downloads/groww_algo_trading_repo

# Set local git config for this repo
git config user.name "rtk707"
git config user.email "your-email@example.com"

# Use HTTPS (will prompt for credentials)
git remote set-url origin https://github.com/rtk707/Groww-Algo-Trading.git

# Push
git push -u origin main
```

## Troubleshooting

If you get permission errors:
1. Check SSH key is added to GitHub account
2. Test SSH: `ssh -T git@github-secondary`
3. Verify remote URL: `git remote -v`
4. Check git config: `git config --list`
