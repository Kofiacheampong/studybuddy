import pytest
import sqlite3
import os
import sys
import tempfile

# Add src directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


@pytest.fixture
def app():
    """Create a test Flask app"""
    # Create temp database for testing
    db_fd, db_path = tempfile.mkstemp()
    
    # Import app and configure for testing
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    
    # Monkey-patch the DB path for this app instance
    import app as app_module
    original_db = app_module.DB
    app_module.DB = db_path
    
    # Initialize test database
    init_test_db(db_path)
    
    yield flask_app
    
    # Cleanup
    app_module.DB = original_db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


def init_test_db(db_path):
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
    
    # Create default "General" topic
    c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
              ('General', 'Default study topic'))
    
    conn.commit()
    conn.close()
