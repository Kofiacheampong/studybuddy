# CI/CD Pipeline Summary

This document provides a quick reference for Study Buddy's CI/CD pipeline.

## What Was Created

### GitHub Actions Workflows (`.github/workflows/ci.yml`)

**Triggers**: Every push to `main`/`develop`, every PR to `main`/`develop`

**Jobs**:
- 🧪 **Test**: Python 3.10/3.11/3.12, pytest, coverage
- 🔒 **Security**: Bandit & Safety vulnerability scanning  
- 🚀 **Deploy**: SSH to production server, pull code, restart app

### Code Quality Configuration

| File | Purpose |
|------|---------|
| `pytest.ini` | Pytest test runner configuration |
| `setup.cfg` | Coverage and code analysis settings |
| `.flake8` | Linting rules (max line length, ignores) |
| `.bandit` | Security scanning configuration |
| `.pre-commit-config.yaml` | Git pre-commit hooks (Black, isort, flake8, Bandit) |

### Testing & Development

| File | Purpose |
|------|---------|
| `tests/conftest.py` | Pytest fixtures and test database setup |
| `tests/test_app.py` | Test cases for routes and features |
| `requirements.txt` | Updated with dev dependencies |

### Scripts & Utilities

| File | Purpose |
|------|---------|
| `setup-dev.sh` | One-command dev environment setup |
| `Makefile` | Common tasks (test, lint, format, security, etc.) |
| `CI_CD_GUIDE.md` | Comprehensive CI/CD documentation |

## Quick Start

### 1. Set Up GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

```
SERVER_HOST      → Your server IP
SERVER_USER      → SSH username  
SERVER_PORT      → SSH port
SSH_PRIVATE_KEY  → SSH private key content
```

### 2. Set Up Local Dev Environment

```bash
bash setup-dev.sh
```

Or manually:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

### 3. Run Tests Locally

```bash
pytest                    # Run all tests
make test                 # Run tests with coverage
make lint                 # Check code quality
make format               # Auto-fix formatting
```

### 4. Commit & Push

Pre-commit hooks run automatically:

```bash
git add .
git commit -m "Your message"  # Pre-commit checks run here
git push origin main          # CI runs on GitHub, then CD deploys
```

## Common Makefile Commands

```bash
make help              # Show all available commands
make install-dev       # Install all dependencies
make test              # Run tests with coverage report
make lint              # Check code formatting/style
make format            # Auto-format code
make security          # Security vulnerability scan
make run               # Start Flask dev server
make clean             # Remove cache/build files
```

## How It Works

### 1️⃣ Developer Pushes Code

```
git push origin main
```

### 2️⃣ GitHub Actions Runs CI

- Install dependencies
- Run tests on Python 3.10/3.11/3.12
- Check linting (flake8, black, isort)
- Run security scans (Bandit, Safety)
- Generate coverage report

### 3️⃣ If All Checks Pass → CD Runs

- SSH into production server
- Pull latest code
- Install dependencies  
- Restart Flask app

### 4️⃣ Production Updated ✅

## Preventing Bad Commits with Pre-commit

Pre-commit hooks run **before** you commit:

```bash
# Install hooks (one-time)
pre-commit install

# They run automatically on git commit
git commit -m "message"  # Hooks check code here

# Manually run against all files
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

## Viewing Pipeline Status

- **GitHub Actions**: https://github.com/Kofiacheampong/studybuddy/actions
- **Workflow Definition**: `.github/workflows/ci.yml`
- **Logs**: Click on workflow run for details

## Testing Coverage

Run locally to see coverage:

```bash
make test
# Opens htmlcov/index.html in browser
```

View on GitHub Actions after successful run.

## Deployment Troubleshooting

### If deployment fails, check:

1. **SSH Secrets are correct**:
   ```bash
   ssh -p SERVER_PORT SERVER_USER@SERVER_HOST "echo test"
   ```

2. **Server directory exists**:
   ```bash
   ssh -p SERVER_PORT SERVER_USER@SERVER_HOST "ls -la /var/www/study-buddy"
   ```

3. **Server has Git & systemd**:
   ```bash
   ssh -p SERVER_PORT SERVER_USER@SERVER_HOST "which git"
   ssh -p SERVER_PORT SERVER_USER@SERVER_HOST "systemctl is-enabled study-buddy"
   ```

4. **View deployment logs**:
   - Go to https://github.com/Kofiacheampong/studybuddy/actions
   - Click latest workflow run
   - Click "deploy" job
   - Expand "Deploy to production server" step

## Project Structure

```
studybuddy/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions config
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   └── test_app.py               # Test cases
├── app.py                        # Flask app
├── requirements.txt              # Dependencies
├── pytest.ini                    # Pytest config
├── setup.cfg                     # Coverage config
├── .flake8                       # Linting config
├── .bandit                       # Security config
├── .pre-commit-config.yaml       # Pre-commit hooks
├── setup-dev.sh                  # Dev setup script
├── Makefile                      # Common commands
├── CI_CD_GUIDE.md                # Full documentation
└── README.md (this file)
```

## Next Steps

1. ✅ Set GitHub Secrets (see Quick Start #1)
2. ✅ Run `bash setup-dev.sh` locally
3. ✅ Make a small change and push to test CI/CD
4. ✅ Monitor workflow at GitHub Actions
5. ✅ Verify deployment to production

## Documentation

- **Full Guide**: See `CI_CD_GUIDE.md`
- **Test Reference**: See `tests/test_app.py`
- **Makefile Help**: Run `make help`

---

**Questions?** Check `CI_CD_GUIDE.md` for detailed explanations of each component.
