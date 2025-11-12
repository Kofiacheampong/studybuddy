import pytest
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    flask_app.config['TESTING'] = True
    
    # Use in-memory database for testing
    os.environ['DATABASE_PATH'] = ':memory:'
    
    with flask_app.test_client() as client:
        with flask_app.app_context():
            # Initialize test database
            init_db(':memory:')
        yield client

@pytest.fixture
def app():
    """Return the Flask app for testing"""
    flask_app.config['TESTING'] = True
    return flask_app

def init_db(db_path):
    """Initialize the test database"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            term TEXT NOT NULL,
            definition TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
