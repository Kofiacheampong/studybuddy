# CI/CD Pipeline Setup Guide for Study Buddy

This guide explains how to use the automated CI/CD pipeline for the Study Buddy Flask application.

## Overview

The CI/CD pipeline consists of:

1. **Continuous Integration (CI)**: Automated testing, linting, and security checks on every push and pull request
2. **Continuous Deployment (CD)**: Automatic deployment to production server on successful main branch push
3. **Pre-commit Hooks**: Local code quality checks before pushing

## How It Works

### GitHub Actions Workflow

The pipeline runs automatically on:
- **Every push** to `main` or `develop` branches
- **Every pull request** to `main` or `develop` branches

### Stage 1: Testing & Linting

Tests run against Python 3.10, 3.11, and 3.12 to ensure compatibility:

```
✅ Install dependencies
✅ Lint code with flake8
✅ Check formatting with Black
✅ Check import ordering with isort
✅ Run unit tests with pytest
✅ Generate coverage report
```

### Stage 2: Security Checks

Security scanning for vulnerabilities:

```
✅ Bandit: Python code security analysis
✅ Safety: Check for known security vulnerabilities in dependencies
```

### Stage 3: Deployment

Automatic deployment to production when:
- All tests pass ✅
- Branch is `main` ✅
- Event is a `push` (not PR) ✅

Deployment actions:
1. SSH into production server
2. Pull latest code from main branch
3. Install dependencies
4. Restart the Flask application

## Setting Up CI/CD

### 1. Create GitHub Secrets

Store sensitive configuration in GitHub repository settings:

Go to: **Settings → Secrets and variables → Actions**

Add these secrets:

| Secret Name | Value |
|------------|-------|
| `SERVER_HOST` | Your server IP address (e.g., `192.168.1.172`) |
| `SERVER_USER` | SSH username (e.g., `kofiarcher`) |
| `SERVER_PORT` | SSH port (e.g., `64295`) |
| `SSH_PRIVATE_KEY` | Your SSH private key content |

**To get your SSH private key:**

```bash
# On your local machine
cat ~/.ssh/id_rsa
```

Copy the entire content (including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`) into the secret.

### 2. Generate SSH Key (if you don't have one)

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""

# Add public key to server
ssh-copy-id -p 64295 -i ~/.ssh/id_rsa.pub kofiarcher@192.168.1.172
```

### 3. Configure Server for CD

Your production server needs:

```bash
# SSH access already configured
# Git installed
sudo apt-get install -y git

# Application directory set up
sudo mkdir -p /var/www/study-buddy
sudo chown kofiarcher:kofiarcher /var/www/study-buddy
cd /var/www/study-buddy
git init
```

### 4. Verify SSH Key Permissions

On your production server:

```bash
# SSH key should have 600 permissions
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

## Local Development - Pre-commit Hooks

Catch issues before pushing:

### Install pre-commit hooks:

```bash
# Install pre-commit package
pip install pre-commit

# Install the git hooks
pre-commit install

# (Optional) Run against all files
pre-commit run --all-files
```

### What the hooks check:

- **Trailing whitespace** removal
- **File endings** fixed
- **YAML syntax** validation
- **File size** limits (1MB max)
- **Debug statements** detection
- **Code formatting** with Black
- **Import ordering** with isort
- **Linting** with flake8
- **Security** with Bandit
- **Python version** compatibility with pyupgrade

### Running pre-commit manually:

```bash
# Check all files
pre-commit run --all-files

# Check specific file
pre-commit run --files app.py

# Bypass hooks (not recommended)
git commit --no-verify
```

## Running Tests Locally

### Run all tests:

```bash
pytest
```

### Run specific test file:

```bash
pytest tests/test_app.py -v
```

### Run with coverage report:

```bash
pytest --cov=. --cov-report=html
```

Opens `htmlcov/index.html` in your browser.

### Run specific test class:

```bash
pytest tests/test_app.py::TestHomePage -v
```

### Run specific test:

```bash
pytest tests/test_app.py::TestHomePage::test_index_page_loads -v
```

## Workflow Examples

### Normal Development Workflow:

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
# (pre-commit hooks run on commit)
git add .
git commit -m "Add new feature"

# 3. Push to GitHub
git push origin feature/my-feature

# 4. Create Pull Request
# CI runs automatically - all checks must pass

# 5. Merge to main
# All CI passes ✅
git checkout main
git merge feature/my-feature
git push origin main

# 6. CD deploys automatically ✅
```

### If Tests Fail:

```bash
# Check what failed
# GitHub Actions shows logs at https://github.com/Kofiacheampong/studybuddy/actions

# Fix the issues locally
# Run tests
pytest

# Run linting
black .
isort .
flake8 .

# Commit and push
git add .
git commit -m "Fix test failures"
git push origin feature/my-feature
```

## Monitoring CI/CD

### View Pipeline Status:

- **GitHub**: https://github.com/Kofiacheampong/studybuddy/actions
- **Workflow file**: `.github/workflows/ci.yml`
- **Branch protection**: Requires passing checks before merge

### Check Test Coverage:

```bash
# After running pytest locally
open htmlcov/index.html
```

Or on GitHub Actions: Check the artifact uploads in the workflow run.

## Troubleshooting

### SSH Connection Failed

**Error**: `Permission denied (publickey)`

**Solution**:
```bash
# Verify key is in authorized_keys on server
cat ~/.ssh/id_rsa.pub | ssh -p 64295 kofiarcher@192.168.1.172 'cat >> ~/.ssh/authorized_keys'

# Verify permissions
ssh -p 64295 kofiarcher@192.168.1.172 'chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'

# Test connection
ssh -p 64295 kofiarcher@192.168.1.172 'echo Connection successful'
```

### Tests Pass Locally But Fail in CI

**Common causes**:
- Python version mismatch (test with all 3 versions)
- Missing environment variables (check CI config)
- File path issues (use absolute paths)

**Solution**:
```bash
# Test with different Python versions
python3.10 -m pytest
python3.11 -m pytest
python3.12 -m pytest
```

### Deployment Fails

**Check server logs**:
```bash
ssh -p 64295 kofiarcher@192.168.1.172 'sudo systemctl status study-buddy'
ssh -p 64295 kofiarcher@192.168.1.172 'sudo journalctl -u study-buddy -n 50'
```

### Pre-commit Hooks Block Commit

**If Black reformats code**:
```bash
# Stage the reformatted files
git add .

# Commit again
git commit -m "Your message"
```

## Best Practices

1. **Always write tests** for new features
2. **Run tests locally** before pushing
3. **Keep secrets in GitHub Secrets**, never in code
4. **Use descriptive commit messages** for clarity
5. **Create feature branches** for work
6. **Create Pull Requests** for review
7. **Monitor CI/CD logs** for issues
8. **Keep dependencies updated** (in requirements.txt)

## Next Steps

1. Set up GitHub Secrets (see Section 1)
2. Install pre-commit hooks locally
3. Run tests to verify setup
4. Make a test push to trigger CI/CD
5. Monitor the workflow run

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pre-commit Framework](https://pre-commit.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
