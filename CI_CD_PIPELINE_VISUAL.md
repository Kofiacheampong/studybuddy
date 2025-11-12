# Study Buddy CI/CD Pipeline - Visual Overview

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DEVELOPER WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

1. LOCAL DEVELOPMENT
   ├── Code changes
   ├── Pre-commit hooks run (BLACK, isort, flake8, Bandit)
   │   ├─ Fix formatting
   │   ├─ Check linting
   │   ├─ Security scan
   │   └─ Python compatibility
   └── git push

2. GITHUB PUSH
   │
   ├─────────────────────────────────┐
   │                                 │
   ▼                                 ▼
┌──────────────────┐        ┌──────────────────┐
│   PULL REQUEST   │        │   PUSH TO MAIN   │
│   (ci only)      │        │   (ci + cd)      │
└──────────────────┘        └──────────────────┘
        │                            │
        ▼                            ▼
   🧪 CI STAGE                 🧪 CI STAGE
   (test only)                 (test → deploy)
```

## CI Pipeline (Continuous Integration)

```
GitHub Push/PR
    │
    ▼
┌─────────────────────────────────────────┐
│         STAGE 1: DEPENDENCIES           │
│  - Set up Python 3.10/3.11/3.12         │
│  - Cache pip                            │
│  - Install requirements.txt             │
└─────────────────────────────────────────┘
    │
    ├────────────┬────────────┬────────────┐
    │            │            │            │
    ▼            ▼            ▼            ▼
 ┌──────┐   ┌──────┐    ┌──────┐    ┌──────┐
 │PY310 │   │PY311 │    │PY312 │    │SECURITY
 │Tests │   │Tests │    │Tests │    │Scan
 └──────┘   └──────┘    └──────┘    └──────┘
    │            │            │            │
    └────────────┼────────────┼────────────┘
                 ▼            ▼
        ┌──────────────────────────┐
        │ STAGE 2: CODE QUALITY    │
        │ - flake8 (linting)       │
        │ - Black (formatting)     │
        │ - isort (imports)        │
        │ - Coverage Report        │
        └──────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌─────────────┐      ┌─────────────────┐
│ All Pass ✅ │      │ Any Fail ❌     │
│             │      │                 │
│ Proceed →   │      │ Block Merge ✋  │
│ to deploy   │      │ Show Logs       │
└─────────────┘      └─────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│   STAGE 3: SECURITY SCANNING            │
│   (if main branch + push event)         │
│   - Bandit (Python security)            │
│   - Safety (dependency vulnerabilities) │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│   STAGE 4: DEPLOYMENT (if main only)    │
│   1. SSH into production server         │
│   2. git pull origin main               │
│   3. pip install -r requirements.txt    │
│   4. systemctl restart study-buddy      │
│   5. Verify app restarted ✅            │
└─────────────────────────────────────────┘
    │
    ▼
 ✅ LIVE IN PRODUCTION
```

## What Gets Tested

```
📋 TEST MATRIX
├─ Python 3.10 ✓
├─ Python 3.11 ✓
├─ Python 3.12 ✓
│
📝 CODE QUALITY
├─ Syntax (flake8)
├─ Formatting (Black)
├─ Imports (isort)
├─ Complexity
├─ Line length
└─ Code coverage

🔒 SECURITY
├─ Python code vulnerabilities (Bandit)
├─ Known dependency CVEs (Safety)
├─ Dangerous functions usage
└─ SQL injection patterns

✅ UNIT TESTS
├─ Homepage loads
├─ Topic CRUD operations
├─ Notes management
├─ Flashcards management
├─ Quiz feature
├─ Error handling (404s)
└─ Database integrity
```

## File Structure

```
studybuddy/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    ← GitHub Actions workflow
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  ← Test fixtures
│   └── test_app.py                  ← Test cases
│
├── .pre-commit-config.yaml          ← Pre-commit hooks
├── .flake8                          ← Flake8 config
├── .bandit                          ← Bandit security config
├── pytest.ini                       ← Pytest config
├── setup.cfg                        ← Coverage config
│
├── Makefile                         ← Development shortcuts
├── setup-dev.sh                     ← Dev environment setup
├── requirements.txt                 ← Updated with dev deps
│
├── CI_CD_GUIDE.md                   ← Full documentation
├── CI_CD_README.md                  ← Quick reference
└── CI_CD_PIPELINE_VISUAL.md         ← This file
```

## Key Workflows

### 🛠️ Local Development Workflow

```bash
# First time setup
bash setup-dev.sh

# Day-to-day development
source venv/bin/activate
code .                    # Make changes
pytest                    # Test locally
make format               # Format code
git add .
git commit -m "msg"       # Pre-commit hooks run
git push origin main      # GitHub CI runs

# Check results
# → https://github.com/Kofiacheampong/studybuddy/actions
```

### 🚀 Feature Branch Workflow

```bash
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature

# Create PR on GitHub
# CI runs (but NO deploy since not main)
# Reviews & approval
# Merge to main → CI + CD runs → Deploy ✅
```

### 🐛 Bug Fix Workflow

```bash
git checkout -b bugfix/my-bug
# ... fix and test ...
make test                 # Verify fix
make lint                 # Code quality
git commit -m "fix: ..."
git push origin bugfix/my-bug
# Create PR, get approval
# Merge → Auto-deployed ✅
```

## Status Checks

```
GitHub Branch Protection Rules:
┌─────────────────────────────────────┐
│ Main branch requires passing:        │
├─────────────────────────────────────┤
│ ✅ test (Python 3.10/3.11/3.12)    │
│ ✅ Code quality (Black, isort, etc) │
│ ✅ Security scans (Bandit, Safety)  │
│ ✅ Coverage reports                 │
│                                     │
│ Before merge allowed: ALL PASS      │
│ Admins can force merge if needed    │
└─────────────────────────────────────┘
```

## Deployment Flow (Main Branch Only)

```
Git Push to main
         │
         ▼
   ┌──────────────┐
   │  CI Passes?  │
   └──────────────┘
         │ YES
         ▼
   ┌──────────────────────────────────┐
   │ Deploy Stage Starts              │
   │ (appleboy/ssh-action)            │
   └──────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ 1. SSH to production server      │
   │    Host: secrets.SERVER_HOST     │
   │    User: secrets.SERVER_USER     │
   │    Port: secrets.SERVER_PORT     │
   │    Key: secrets.SSH_PRIVATE_KEY  │
   └──────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ 2. Pull latest code              │
   │    cd /var/www/study-buddy       │
   │    git pull origin main          │
   └──────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ 3. Install/update dependencies   │
   │    source venv/bin/activate      │
   │    pip install -r requirements   │
   └──────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ 4. Restart application           │
   │    sudo systemctl restart        │
   │    study-buddy                   │
   └──────────────────────────────────┘
         │
         ▼
   ┌──────────────────────────────────┐
   │ ✅ LIVE IN PRODUCTION            │
   │                                  │
   │ Users access updated app!        │
   └──────────────────────────────────┘
```

## GitHub Secrets Required

```
GitHub Settings → Secrets and variables → Actions

SECRET NAME      │ EXAMPLE VALUE                  │ WHERE TO GET IT
─────────────────┼────────────────────────────────┼─────────────────────
SERVER_HOST      │ 192.168.1.172                  │ Your server IP
SERVER_USER      │ kofiarcher                     │ SSH username
SERVER_PORT      │ 64295                          │ SSH port
SSH_PRIVATE_KEY  │ -----BEGIN RSA PRIVATE KEY--   │ ~/.ssh/id_rsa
                 │ (full key content)             │ cat ~/.ssh/id_rsa
```

## Common Commands

```bash
make help                # Show all commands
make install-dev         # Install dev dependencies
make test                # Run tests with coverage
make lint                # Check code quality
make format              # Auto-fix formatting
make security            # Security vulnerability scan
make run                 # Start development server
make clean               # Remove build artifacts
pre-commit run --all-files  # Run pre-commit manually
```

## Monitoring & Debugging

### View CI/CD Status
```
https://github.com/Kofiacheampong/studybuddy/actions
```

### Common Issues & Fixes

```
❌ SSH Connection Failed
   → Verify SSH_PRIVATE_KEY secret
   → Check server IP and port
   → Verify SSH key on server: ~/.ssh/authorized_keys

❌ Tests Fail in CI
   → Run locally: pytest
   → Check Python version compatibility
   → Review log output on GitHub Actions

❌ Deployment Fails
   → SSH and check server: sudo systemctl status study-buddy
   → View logs: sudo journalctl -u study-buddy -n 50
   → Verify directory: /var/www/study-buddy exists

❌ Pre-commit Blocks Commit
   → Run: pre-commit run --all-files
   → Code will be auto-fixed (mostly)
   → Re-stage and commit again
```

## Performance

```
TYPICAL TIMES:
├─ Pre-commit hooks:      5-15 seconds
├─ CI Pipeline:           2-5 minutes
├─ Security Scans:        1-2 minutes
└─ Deployment:            1-2 minutes

Total: ~7-10 minutes from push to live
```

## Security Considerations

```
✅ IMPLEMENTATION
├─ SSH keys for authentication (no passwords)
├─ GitHub Secrets for sensitive data
├─ Pre-commit security scanning
├─ CI/CD security vulnerability checks
├─ No credentials in code/logs
└─ Signed commits recommended

🔒 BEST PRACTICES
├─ Rotate SSH keys regularly
├─ Use strong passphrases
├─ Monitor GitHub Actions logs
├─ Review security scan reports
├─ Keep dependencies updated
└─ Test deployments in staging first
```

## Next Steps

1. **Set GitHub Secrets** (see CI_CD_GUIDE.md § Setting Up CI/CD)
2. **Test Locally**:
   ```bash
   bash setup-dev.sh
   make test
   ```
3. **Make a Test Push**:
   ```bash
   git add .
   git commit -m "test: verify CI/CD pipeline"
   git push origin main
   ```
4. **Monitor Workflow**: Visit Actions tab on GitHub
5. **Verify Deployment**: Check production server

---

**For more details**, see:
- `CI_CD_GUIDE.md` - Complete setup & troubleshooting guide
- `CI_CD_README.md` - Quick reference
- `.github/workflows/ci.yml` - Workflow definition
