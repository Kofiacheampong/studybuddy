.PHONY: help install install-dev test lint format security run clean pre-commit docs

help:
	@echo "Study Buddy Development Commands"
	@echo "================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             - Run all tests with coverage"
	@echo "  make test-fast        - Run tests without coverage"
	@echo "  make test-watch       - Run tests in watch mode"
	@echo "  make lint             - Run all linters (flake8, black, isort)"
	@echo "  make format           - Auto-format code (black, isort)"
	@echo "  make security         - Run security checks (bandit, safety)"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit       - Run pre-commit hooks on all files"
	@echo ""
	@echo "Development:"
	@echo "  make run              - Run Flask development server"
	@echo "  make clean            - Remove build artifacts and cache files"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             - Generate coverage HTML report"
	@echo ""

install:
	pip install --upgrade pip
	pip install Flask requests python-dotenv anthropic gunicorn

install-dev:
	pip install --upgrade pip
	pip install -r requirements.txt
	pre-commit install

test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing

test-fast:
	pytest tests/ -v --tb=short

test-watch:
	pytest-watch tests/ -n

lint:
	@echo "Running flake8..."
	flake8 . --max-line-length=127
	@echo "Running black check..."
	black . --check --diff
	@echo "Running isort check..."
	isort . --check-only --diff
	@echo "✓ All linting checks passed!"

format:
	@echo "Running black..."
	black .
	@echo "Running isort..."
	isort .
	@echo "✓ Code formatted!"

security:
	@echo "Running bandit security checks..."
	bandit -r . -f json -o bandit-report.json || true
	@echo "Running safety vulnerability checks..."
	safety check --json || true
	@echo "✓ Security checks completed!"

pre-commit:
	pre-commit run --all-files

run:
	flask run

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "bandit-report.json" -delete
	@echo "✓ Cleaned up build artifacts!"

docs:
	@echo "Opening coverage report..."
	@if [ -f htmlcov/index.html ]; then \
		python3 -m http.server --directory htmlcov 8000; \
	else \
		echo "Coverage report not found. Run 'make test' first."; \
	fi

.DEFAULT_GOAL := help
