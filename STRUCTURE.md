# Project Structure

The StudyBuddy project is now organized with a clean, professional structure:

```
studybuddy/
├── src/                          # All Python source code
│   ├── __init__.py              # Package marker
│   ├── app.py                   # Main Flask application
│   └── topics_manager.py        # Topics blueprint
│
├── templates/                    # Flask HTML templates
│   ├── base.html
│   ├── index.html
│   ├── notes.html
│   ├── flashcards.html
│   ├── quiz.html
│   └── topic_view.html
│
├── static/                       # CSS, JavaScript, assets
│   └── style.css
│
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest fixtures and configuration
│   └── test_app.py              # Unit tests (10 tests)
│
├── docs/                         # Documentation files
│   ├── RENDER_DEPLOYMENT.md     # Render deployment guide
│   ├── FREE_HOSTING_OPTIONS.md  # Hosting comparison
│   ├── PRODUCTION_SERVER_OPTIONS.md
│   ├── DEPLOY_TO_HOME_SERVER.md
│   ├── AUTO_DEPLOY_SETUP.md
│   └── ... (other guides)
│
├── config/                       # Configuration files
│   ├── .env                     # Environment variables
│   ├── .flake8                  # Linting configuration
│   ├── setup.cfg                # Setup tools config
│   ├── pytest.ini               # Pytest configuration
│   ├── .pre-commit-config.yaml  # Pre-commit hooks
│   ├── .bandit                  # Security scanning
│   └── Makefile                 # Build commands
│
├── data/                         # Database files (git-ignored)
│   └── study_buddy.db           # SQLite database
│
├── scripts/                      # Utility scripts
│   ├── deploy.sh                # Deployment script
│   ├── setup-dev.sh             # Development setup
│   └── update-app.sh            # Update script
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
│
├── wsgi.py                       # WSGI entry point for production
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── .env -> config/.env          # Symlink to config/.env
└── README.md                     # Project README
```

## Running the Application

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python wsgi.py
# OR
python -m flask run
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Linting & Code Quality
```bash
# Lint with flake8
flake8 src/ tests/

# Format with black (optional)
black src/ tests/

# Sort imports with isort (optional)
isort src/ tests/
```

## Key Configuration Files

**config/.flake8** - Linting rules  
**config/pytest.ini** - Test configuration  
**config/.env** - Environment variables (git-ignored)  
**config/.pre-commit-config.yaml** - Git pre-commit hooks

## Database

The SQLite database is stored in the `data/` directory:
- Development: `data/study_buddy.db`
- Production: `/var/www/study-buddy/data/study_buddy.db`

The database path is automatically configured based on the `FLASK_ENV` environment variable.

## Deployment

For deployment instructions, see the relevant guide in `docs/`:
- **Render.com**: `docs/RENDER_DEPLOYMENT.md`
- **Home Server**: `docs/DEPLOY_TO_HOME_SERVER.md`
- **Other Options**: `docs/FREE_HOSTING_OPTIONS.md`

## Python Path Configuration

When running from the root directory:
- Flask imports from `src/`
- Tests import from `src/` (via pytest.ini configuration)
- `.env` symlink points to `config/.env`

This allows clean separation of concerns while maintaining simple import statements.
