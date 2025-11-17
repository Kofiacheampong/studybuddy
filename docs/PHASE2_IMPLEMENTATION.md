# Phase 2 Implementation: Topic Management Routes

Ready to add full topic support? Here's the complete code to add.

## File 1: Create `topics_manager.py`

This file handles all topic CRUD operations.

```python
# topics_manager.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3
from app import DB

bp = Blueprint('topics', __name__, url_prefix='/topics')

@bp.route('/')
def list_topics():
    """Display all study topics"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics ORDER BY name')
    topics = c.fetchall()
    conn.close()
    
    # Calculate stats for each topic
    topic_stats = []
    for topic in topics:
        topic_id = topic[0]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM notes WHERE topic_id = ?', (topic_id,))
        note_count = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM flashcards WHERE topic_id = ?', (topic_id,))
        card_count = c.fetchone()[0]
        conn.close()
        
        topic_stats.append({
            'id': topic[0],
            'name': topic[1],
            'description': topic[2],
            'notes': note_count,
            'flashcards': card_count
        })
    
    return render_template('topics.html', topics=topic_stats)

@bp.route('/create', methods=['GET', 'POST'])
def create_topic():
    """Create a new study topic"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            return render_template('create_topic.html', error="Topic name is required")
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        try:
            c.execute('INSERT INTO topics (name, description) VALUES (?, ?)', 
                      (name, description))
            conn.commit()
            topic_id = c.lastrowid
            conn.close()
            return redirect(url_for('topics.view_topic', topic_id=topic_id))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('create_topic.html', error="Topic already exists")
        except Exception as e:
            conn.close()
            return render_template('create_topic.html', error=f"Error: {str(e)}")
    
    return render_template('create_topic.html')

@bp.route('/<int:topic_id>')
def view_topic(topic_id):
    """View a specific topic with stats"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    
    if not topic:
        conn.close()
        return "Topic not found", 404
    
    c.execute('SELECT COUNT(*) FROM notes WHERE topic_id = ?', (topic_id,))
    note_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM flashcards WHERE topic_id = ?', (topic_id,))
    card_count = c.fetchone()[0]
    
    conn.close()
    
    return render_template('topic_view.html', 
                         topic={'id': topic[0], 'name': topic[1], 'description': topic[2]},
                         note_count=note_count,
                         card_count=card_count)

@bp.route('/<int:topic_id>/edit', methods=['GET', 'POST'])
def edit_topic(topic_id):
    """Edit topic details"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    conn.close()
    
    if not topic:
        return "Topic not found", 404
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            return render_template('edit_topic.html', topic=topic, error="Topic name required")
        
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        try:
            c.execute('UPDATE topics SET name = ?, description = ? WHERE id = ?',
                      (name, description, topic_id))
            conn.commit()
            conn.close()
            return redirect(url_for('topics.view_topic', topic_id=topic_id))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('edit_topic.html', topic=topic, error="Topic name already exists")
    
    return render_template('edit_topic.html', topic={'id': topic[0], 'name': topic[1], 'description': topic[2]})

@bp.route('/<int:topic_id>/delete', methods=['POST'])
def delete_topic(topic_id):
    """Delete a topic and all associated notes/flashcards"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT name FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    
    if not topic:
        conn.close()
        return "Topic not found", 404
    
    # Delete is cascading (set up in schema with ON DELETE CASCADE)
    c.execute('DELETE FROM topics WHERE id = ?', (topic_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('topics.list_topics'))
```

## File 2: Update `app.py`

Add these lines to register the blueprint:

```python
# At the top of app.py, after other imports
from topics_manager import bp as topics_bp

# After app = Flask(__name__), add:
app.register_blueprint(topics_bp)
```

## File 3: Update routes to be topic-aware

Replace the `/notes` route in `app.py`:

```python
@app.route('/topics/<int:topic_id>/notes', methods=['GET', 'POST'])
def notes(topic_id):
    # Verify topic exists
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    if not topic:
        conn.close()
        return "Topic not found", 404
    
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            c.execute('INSERT INTO notes (topic_id, content) VALUES (?, ?)', 
                      (topic_id, content))
            conn.commit()
        conn.close()
        return redirect(url_for('notes', topic_id=topic_id))
    
    c.execute('SELECT * FROM notes WHERE topic_id = ? ORDER BY created_at DESC', 
              (topic_id,))
    notes_list = c.fetchall()
    conn.close()
    
    return render_template('notes.html', 
                         notes=notes_list, 
                         topic=topic,
                         topic_id=topic_id)

@app.route('/topics/<int:topic_id>/delete_note/<int:note_id>', methods=['POST'])
def delete_note(topic_id, note_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id = ? AND topic_id = ?', (note_id, topic_id))
    conn.commit()
    conn.close()
    return redirect(url_for('notes', topic_id=topic_id))

@app.route('/topics/<int:topic_id>/flashcards', methods=['GET', 'POST'])
def flashcards(topic_id):
    # Verify topic exists
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    if not topic:
        conn.close()
        return "Topic not found", 404
    
    if request.method == 'POST':
        if 'raw_text' in request.form:
            # AI-generated flashcards
            if not client:
                return jsonify({"error": "AI features disabled"}), 400
            
            try:
                raw_text = request.form['raw_text']
                prompt = f"Generate 5 flashcards. Format as 'Term: Definition':\n\n{raw_text}"
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                flashcards_text = response.content[0].text.strip()
                
                lines = flashcards_text.split('\n')
                for line in lines:
                    if ':' in line:
                        term, definition = line.split(':', 1)
                        term = term.strip()
                        definition = definition.strip()
                        if term and definition:
                            c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', 
                                      (topic_id, term, definition))
                
                conn.commit()
                return jsonify({"flashcards": flashcards_text})
            except Exception as e:
                return jsonify({"error": f"Error: {str(e)}"}), 500
        else:
            # Manual flashcard creation
            term = request.form['term'].strip()
            definition = request.form['definition'].strip()
            if term and definition:
                c.execute('INSERT INTO flashcards (topic_id, term, definition) VALUES (?, ?, ?)', 
                          (topic_id, term, definition))
                conn.commit()
            conn.close()
            return redirect(url_for('flashcards', topic_id=topic_id))
    
    c.execute('SELECT * FROM flashcards WHERE topic_id = ? ORDER BY created_at DESC', 
              (topic_id,))
    fc_list = c.fetchall()
    conn.close()
    
    return render_template('flashcards.html', 
                         flashcards=fc_list,
                         topic=topic,
                         topic_id=topic_id)

@app.route('/topics/<int:topic_id>/quiz', methods=['GET', 'POST'])
def quiz(topic_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM topics WHERE id = ?', (topic_id,))
    topic = c.fetchone()
    if not topic:
        conn.close()
        return "Topic not found", 404
    
    if request.method == 'POST':
        c.execute('SELECT * FROM flashcards WHERE topic_id = ?', (topic_id,))
        cards = c.fetchall()
        
        score = 0
        for card in cards:
            card_id = str(card[0])
            if card_id in request.form:
                user_answer = request.form[card_id].strip().lower()
                correct_answer = card[3].strip().lower()  # definition is at index 3
                if user_answer in correct_answer or correct_answer in user_answer:
                    score += 1
        
        conn.close()
        return render_template('quiz.html', 
                             submitted=True, 
                             score=score, 
                             cards=cards,
                             topic=topic)
    
    c.execute('SELECT * FROM flashcards WHERE topic_id = ? ORDER BY RANDOM() LIMIT 10', 
              (topic_id,))
    cards = c.fetchall()
    conn.close()
    
    if not cards:
        return redirect(url_for('flashcards', topic_id=topic_id))
    
    return render_template('quiz.html', 
                         submitted=False, 
                         cards=cards,
                         topic=topic)
```

## File 4: Create `templates/topics.html`

```html
{% extends 'base.html' %}
{% block content %}
<div class="container mt-5">
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Study Topics</h2>
    <a href="{{ url_for('topics.create_topic') }}" class="btn btn-primary">
      + New Topic
    </a>
  </div>
  
  {% if topics %}
    <div class="row">
      {% for topic in topics %}
      <div class="col-md-4 mb-4">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ topic.name }}</h5>
            <p class="card-text text-muted">{{ topic.description }}</p>
            <div class="small mb-3">
              <span class="badge bg-info">{{ topic.notes }} notes</span>
              <span class="badge bg-success">{{ topic.flashcards }} cards</span>
            </div>
          </div>
          <div class="card-footer bg-white border-top">
            <a href="{{ url_for('topics.view_topic', topic_id=topic.id) }}" 
               class="btn btn-sm btn-primary me-2">Study</a>
            <a href="{{ url_for('topics.edit_topic', topic_id=topic.id) }}" 
               class="btn btn-sm btn-warning me-2">Edit</a>
            <form method="POST" 
                  action="{{ url_for('topics.delete_topic', topic_id=topic.id) }}" 
                  style="display:inline;">
              <button type="submit" class="btn btn-sm btn-danger"
                      onclick="return confirm('Delete this topic and all its data?')">
                Delete
              </button>
            </form>
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  {% else %}
    <div class="alert alert-info">
      No topics yet. <a href="{{ url_for('topics.create_topic') }}">Create your first topic</a>!
    </div>
  {% endif %}
</div>
{% endblock %}
```

## File 5: Create `templates/create_topic.html`

```html
{% extends 'base.html' %}
{% block content %}
<div class="container mt-5" style="max-width: 600px;">
  <h2>Create New Topic</h2>
  
  {% if error %}
    <div class="alert alert-danger">{{ error }}</div>
  {% endif %}
  
  <form method="POST">
    <div class="mb-3">
      <label for="name" class="form-label">Topic Name *</label>
      <input type="text" class="form-control" id="name" name="name" 
             placeholder="e.g., AWS, Cybersecurity, Networking" required>
      <small class="text-muted">Examples: AWS, Cybersecurity, Networking, DevOps</small>
    </div>
    
    <div class="mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea class="form-control" id="description" name="description" 
                rows="3" placeholder="Optional description of this topic..."></textarea>
    </div>
    
    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-primary">Create Topic</button>
      <a href="{{ url_for('topics.list_topics') }}" class="btn btn-secondary">Cancel</a>
    </div>
  </form>
</div>
{% endblock %}
```

## Implementation Checklist

- [ ] Create `topics_manager.py` file
- [ ] Add blueprint registration in `app.py`
- [ ] Update routes in `app.py` to accept `topic_id`
- [ ] Create `templates/topics.html`
- [ ] Create `templates/create_topic.html`
- [ ] Test creating a topic
- [ ] Test adding notes to topic
- [ ] Test adding flashcards to topic
- [ ] Test quiz for topic
- [ ] Update navbar with link to topics

## Test Commands

```bash
# Start app
python app.py

# Navigate to:
# http://localhost:5000/topics
# http://localhost:5000/topics/create
```

---

This completes Phase 2! You'll have full topic management ready to use.
