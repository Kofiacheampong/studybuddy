import pytest
import sqlite3
import os
import sys
import tempfile

# Add src directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Session-level fixture to ensure data directory exists"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)


@pytest.fixture
def app():
    """Create a test Flask app"""
    # Create temp database for testing
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Import app and configure for testing
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    
    # Monkey-patch DB in both root app.py and src/app.py
    import app as root_app_module
    original_db = root_app_module.DB
    root_app_module.DB = db_path
    
    # Also patch src/app.py directly
    try:
        import src.app as src_app_module
        src_original_db = src_app_module.DB
        src_app_module.DB = db_path
    except (ImportError, AttributeError):
        src_original_db = None
    
    # Also patch topics_manager
    try:
        import topics_manager
        original_topics_db = topics_manager.DB
        topics_manager.DB = db_path
    except (ImportError, AttributeError):
        original_topics_db = None
    
    # Initialize test database
    init_test_db(db_path)
    
    yield flask_app
    
    # Cleanup
    root_app_module.DB = original_db
    if src_original_db is not None:
        src_app_module.DB = src_original_db
    if original_topics_db is not None:
        topics_manager.DB = original_topics_db
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
