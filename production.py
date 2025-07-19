# Production configuration for OCI Study Buddy

import os
from app import app, init_db

# Production settings
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Database path for production
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'oci_study.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Update the DB constant in app module
import app as app_module
app_module.DB = DB_PATH

if __name__ == '__main__':
    # Initialize database on first run
    init_db()
    
    # Run with gunicorn in production, this is just for testing
    app.run(host='127.0.0.1', port=5001, debug=False)