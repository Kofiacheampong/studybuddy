# Universal Study Buddy - Migration Guide

## Overview

Your Study Buddy app has been transformed from OCI-specific to a **universal multi-topic study platform**. You can now create study materials for:
- 🏢 AWS, Azure, GCP
- 🔐 Cybersecurity, Network Security
- 🕸️ Networking (TCP/IP, DNS, VPN)
- 📊 Data Science, Machine Learning
- 🔄 DevOps, CI/CD
- 💾 Databases
- **Any other topic!**

## What Changed

### 1. **Database Schema** - Now Topic-Aware
```
OLD:
┌─ notes (id, content)
└─ flashcards (id, term, definition)

NEW:
┌─ topics (id, name, description) ← NEW!
├─ notes (id, topic_id, content, created_at)
└─ flashcards (id, topic_id, term, definition, created_at)
```

### 2. **Naming Convention**
- Database: `oci_study.db` → `study_buddy.db`
- Directory: `/var/www/oci-study-buddy/` → `/var/www/study-buddy/`
- App name: "OCI Study Buddy" → "Study Buddy"
- AI prompts: Now topic-agnostic

### 3. **Backend Routes** - Now Topic-Aware
```python
# OLD
/notes                → All notes
/flashcards           → All flashcards
/quiz                 → Quiz on all cards

# NEW (Recommended Implementation)
/topics                      → List all topics
/topics/create               → Create new topic
/topics/<topic_id>/notes     → Notes for specific topic
/topics/<topic_id>/flashcards → Flashcards for topic
/topics/<topic_id>/quiz      → Quiz for topic
```

## Implementation Steps

### Phase 1: Database Migration ✅ (DONE)
- [x] Updated schema with topics table
- [x] Added foreign keys for data integrity
- [x] Added timestamps for tracking

### Phase 2: Create Topic Management (NEXT)

Create a new `topics_manager.py`:

```python
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

bp = Blueprint('topics', __name__, url_prefix='/topics')

@bp.route('/')
def list_topics():
    """Display all study topics"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics')
    topics = c.fetchall()
    conn.close()
    return render_template('topics.html', topics=topics)

@bp.route('/create', methods=['GET', 'POST'])
def create_topic():
    """Create a new study topic"""
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            return "Topic name required", 400
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
                      (name, description))
            conn.commit()
            topic_id = c.lastrowid
        except sqlite3.IntegrityError:
            return "Topic already exists", 400
        finally:
            conn.close()
        
        return redirect(url_for('topics.view_topic', topic_id=topic_id))
    
    return render_template('create_topic.html')

@bp.route('/<int:topic_id>')
def view_topic(topic_id):
    """View a specific topic"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    conn.close()
    
    if not topic:
        return "Topic not found", 404
    
    return render_template('topic_view.html', topic=topic)

@bp.route('/<int:topic_id>/delete', methods=['POST'])
def delete_topic(topic_id):
    """Delete a topic and all associated notes/flashcards"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM topics WHERE id = ?', (topic_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('topics.list_topics'))
```

### Phase 2: Update Routes in app.py

```python
# Register blueprint
from topics_manager import bp as topics_bp
app.register_blueprint(topics_bp)

# Update existing routes to accept topic_id
@app.route('/topics/<int:topic_id>/notes', methods=['GET', 'POST'])
def notes(topic_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            c.execute('INSERT INTO notes (topic_id, content) VALUES (?, ?)', 
                      (topic_id, content))
            conn.commit()
        return redirect(url_for('notes', topic_id=topic_id))
    
    c.execute('SELECT * FROM notes WHERE topic_id = ? ORDER BY created_at DESC', 
              (topic_id,))
    notes = c.fetchall()
    conn.close()
    return render_template('notes.html', notes=notes, topic_id=topic_id)
```

### Phase 3: UI Templates

**Create `templates/topics.html`:**
```html
{% extends 'base.html' %}
{% block content %}
<div class="container mt-4">
  <h2>Study Topics</h2>
  
  <a href="{{ url_for('topics.create_topic') }}" class="btn btn-primary mb-3">
    + New Topic
  </a>
  
  <div class="row">
    {% for topic in topics %}
    <div class="col-md-4 mb-3">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ topic[1] }}</h5>
          <p class="card-text">{{ topic[2] }}</p>
          <a href="{{ url_for('topics.view_topic', topic_id=topic[0]) }}" 
             class="btn btn-sm btn-primary">Study</a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</div>
{% endblock %}
```

## Migration Path

### For Existing Data (OCI)

```sql
-- Keep your existing OCI data by assigning it to a topic
INSERT INTO topics (name, description) 
VALUES ('Oracle Cloud Infrastructure', 'OCI certification study materials');

UPDATE notes SET topic_id = 1;
UPDATE flashcards SET topic_id = 1;
```

### For New Data

1. Go to `/topics/create`
2. Create new topic (e.g., "AWS", "Cybersecurity")
3. Start adding notes/flashcards for that topic

## Benefits of Multi-Topic Architecture

| Aspect | Before | After |
|--------|--------|-------|
| **Topics** | Only OCI | Unlimited topics |
| **Organization** | All mixed together | Organized by topic |
| **Scalability** | Limited | Multi-user, multi-topic |
| **Reusability** | One-off app | Universal platform |
| **Collaboration** | N/A | Can share topics |

## Next Steps

1. ✅ Update database schema
2. 🔄 Update app.py with topic routes
3. 🎨 Create topic management UI
4. 📝 Migrate existing OCI data
5. 🧪 Test with new topics
6. 🚀 Deploy to production

## Rollback

If needed, the old database is backed up. To restore:
```bash
mv oci_study.db oci_study.db.bak
# Old data is safe to reference
```

## Questions?

Check these files:
- `app.py` - Route definitions
- `templates/` - UI templates
- Database schema documentation

---

**Status**: Phase 1 Complete ✅  
**Next**: Phase 2 - Topic Management Routes  
**Timeline**: Can implement phases 2-3 based on your priorities
