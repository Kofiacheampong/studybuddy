"""Database connection and utilities for SQLite and PostgreSQL"""
import os
import sqlite3
from urllib.parse import urlparse

# Check if we should use PostgreSQL (AWS RDS) or SQLite
DATABASE_URL = os.getenv('DATABASE_URL')
USE_POSTGRES = DATABASE_URL is not None and DATABASE_URL.startswith('postgres')

if USE_POSTGRES:
    import psycopg2
    import psycopg2.extras

def get_db_connection():
    """Get database connection based on environment"""
    if USE_POSTGRES:
        # Parse DATABASE_URL for PostgreSQL connection
        url = urlparse(DATABASE_URL)
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    else:
        # Use SQLite for development
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'data', 'study_buddy.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return sqlite3.connect(db_path)

def init_database():
    """Initialize database tables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if USE_POSTGRES:
            print(f"Initializing PostgreSQL database at: {urlparse(DATABASE_URL).hostname}")
            # PostgreSQL DDL
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    topic_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id SERIAL PRIMARY KEY,
                    topic_id INTEGER NOT NULL,
                    term TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
                )
            """)
        else:
            print(f"Initializing SQLite database")
            # SQLite DDL
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_id INTEGER NOT NULL,
                    term TEXT NOT NULL,
                    definition TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(topic_id) REFERENCES topics(id) ON DELETE CASCADE
                )
            """)
        
        conn.commit()
        
        # Create default topic if none exist
        cursor.execute('SELECT COUNT(*) FROM topics')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(
                'INSERT INTO topics (name, description) VALUES (%s, %s)' if USE_POSTGRES 
                else 'INSERT INTO topics (name, description) VALUES (?, ?)',
                ('General', 'Default study topic')
            )
            conn.commit()
        
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def get_placeholder():
    """Return the correct placeholder for SQL queries (%s for Postgres, ? for SQLite)"""
    return '%s' if USE_POSTGRES else '?'

# For backwards compatibility - expose a get_db function
def get_db():
    """Alias for get_db_connection for compatibility"""
    return get_db_connection()
