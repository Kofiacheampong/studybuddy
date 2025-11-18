"""Root-level app.py wrapper for Gunicorn compatibility."""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask app from src/app.py (use src module notation)
import src.app as src_app
app = src_app.app

if __name__ == "__main__":
    app.run()
