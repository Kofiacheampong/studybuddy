"""WSGI entry point for Flask application"""
import sys
import os

# Add src directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import app

if __name__ == "__main__":
    app.run()
