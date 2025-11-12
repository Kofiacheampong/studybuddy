# GitHub Secrets Setup for Auto-Deployment

## Quick Setup Guide

### Step 1: Get Your Server Information

```bash
# Your server details (from your deploy.sh)
Server IP: 192.168.1.172
SSH User: kofiarcher
SSH Port: 64295
```

### Step 2: Get Your SSH Private Key

```bash
# Print your SSH private key
cat ~/.ssh/id_rsa
```

Copy the **entire output** including:
```
-----BEGIN RSA PRIVATE KEY-----
[... key content ...]
-----END RSA PRIVATE KEY-----
```

### Step 3: Add Secrets to GitHub

1. Go to: https://github.com/Kofiacheampong/studybuddy/settings/secrets/actions
2. Click "New repository secret"
3. Add these 4 secrets:

#### Secret 1: SERVER_HOST
- **Name**: `SERVER_HOST`
- **Value**: `192.168.1.172`

#### Secret 2: SERVER_USER
- **Name**: `SERVER_USER`
- **Value**: `kofiarcher`

#### Secret 3: SERVER_PORT
- **Name**: `SERVER_PORT`
- **Value**: `64295`

#### Secret 4: SSH_PRIVATE_KEY
- **Name**: `SSH_PRIVATE_KEY`
- **Value**: [Paste entire private key from `cat ~/.ssh/id_rsa`]

### Step 4: Verify Secrets Are Set

After adding all 4 secrets, you should see them listed on the Secrets page with a green checkmark.

### Step 5: Test Auto-Deployment

1. Make a small change to your code:
   ```bash
   git add .
   git commit -m "test: verify auto-deployment"
   git push origin main
   ```

2. Go to GitHub Actions to watch it deploy:
   https://github.com/Kofiacheampong/studybuddy/actions

3. The workflow should:
   - ✅ Run tests
   - ✅ Run linting
   - ✅ Run security checks
   - ✅ **Deploy to production server** (new!)

## Production Server Setup (if needed)

If your production server isn't already set up, run:

```bash
./deploy.sh
```

This will:
- SSH to your server
- Create `/var/www/study-buddy` directory
- Install dependencies
- Set up systemd service
- Configure nginx reverse proxy
- Start the application

## How Auto-Deploy Works

```
You push code to main
    ↓
GitHub detects push
    ↓
CI/CD Pipeline runs:
  - Tests ✅
  - Linting ✅
  - Security ✅
    ↓
All pass? YES
    ↓
Deploy job runs:
  - SSH to production server
  - git pull latest code
  - Install dependencies
  - Restart Flask app
    ↓
Production Updated ✅
```

## Troubleshooting

### If deployment fails:

1. **Check SSH key is correct**
   ```bash
   cat ~/.ssh/id_rsa
   ```
   Make sure you copied the entire key including BEGIN/END lines.

2. **Check server is accessible**
   ```bash
   ssh -p 64295 kofiarcher@192.168.1.172 "echo Test successful"
   ```

3. **View GitHub Actions logs**
   - Go to: https://github.com/Kofiacheampong/studybuddy/actions
   - Click the failed workflow
   - Click "deploy" job
   - Expand "Deploy to production server" step
   - See the error message

4. **Check server status**
   ```bash
   ssh -p 64295 kofiarcher@192.168.1.172 "sudo systemctl status study-buddy"
   ```

### If tests fail:

The deploy job won't run if tests fail. Fix the issues:
```bash
pytest tests/ -v
# Fix any failing tests
git commit -am "fix: resolve test failures"
git push origin main
```

## Auto-Deploy Workflow Details

The workflow file at `.github/workflows/ci.yml` defines:

- **Test job**: Runs on Python 3.10, 3.11, 3.12
- **Lint job**: Checks code quality with flake8
- **Security job**: Scans for vulnerabilities with Bandit
- **Deploy job**: 
  - Depends on: test, lint, security jobs
  - Only runs: if all jobs pass + main branch + push event
  - Uses: appleboy/ssh-action to SSH to server
  - Executes: git pull, pip install, systemctl restart

## What Gets Deployed

When auto-deploy runs, it:
1. SSHes into `192.168.1.172:64295` as `kofiarcher`
2. Goes to `/var/www/study-buddy`
3. Pulls latest code: `git pull origin main`
4. Activates venv: `source venv/bin/activate`
5. Installs deps: `pip install -r requirements.txt`
6. Restarts app: `sudo systemctl restart study-buddy`

## Next Steps

1. Add the 4 GitHub Secrets
2. Make a test commit
3. Push to main
4. Watch GitHub Actions deploy
5. Verify app is updated on production

---

For more info, see `.github/workflows/ci.yml` in your repo.
